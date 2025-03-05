import datetime

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import PydanticToolsParser, JsonOutputToolsParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from db import llm
from schema import AnswerQuestion, ReportIdentifier

load_dotenv()


parser_tool = JsonOutputToolsParser(return_id=True)
parser_pydantic = PydanticToolsParser(tools=[AnswerQuestion, ReportIdentifier])
gaurd_rail = """
        {}

        Return the response strictly as a valid JSON array of objects, where each object contains column names as keys and corresponding values. Do not include any surrounding text, explanations, or extra attributes. Ensures the response is a valid JSON string, not a markdown-embedded JSON block."
        """

report_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
     [Timestamp: {timestamp}]

    You are an intelligent database assistant responsible for identifying the type of report a user wants to generate.

    ### **Available Reports:**
    1. **NET_SALES**  
       - Used for generating a net sales report.  
       - Requires data from the following databases: **TRANSACTION_DB, MASTER_DATA_DB, USER_MANAGEMENT_DB**.  
       - Use this when the query involves total revenue, sales breakdowns, or net income calculations.  

    2. **TRANSACTION_SUMMARY**  
       - Used for summarizing transactions.  
       - Requires data from: **TRANSACTION_DB**.  
       - Use this if the query involves transaction details, payment summaries, or financial activity logs.  

    3. **USER_ACTIVITY**  
       - Tracks user account activity.  
       - Requires data from: **USER_MANAGEMENT_DB**.  
       - Use this if the query involves user logins, profile changes, or engagement patterns.    

    ### **Task:**
    Analyze the user's request and determine the most relevant report type along with its associated data sources.

    ### **Response Format:**
    - **Report Name:** <Best-matching report>  
    - **Required Databases:** <List of relevant databases>  
    - **Reasoning:** <Explain why this report is relevant>  

    Ensure the response is clear, accurate, and well-justified.
    """,
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

first_responder_prompt = report_prompt_template.partial(
    timestamp=lambda: datetime.datetime.now().isoformat()
)
first_responder = first_responder_prompt | llm.bind_tools(
    tools=[ReportIdentifier], tool_choice="ReportIdentifier"
)
first_responder_chain = first_responder | parser_pydantic

if __name__ == "__main__":
    messages = [
        "Generate net sales report for the AY 2024-25.",
        "Generate account activity summary for last month.",
    ]

    for msg in messages:
        print("Query: ", msg)
        human_message = HumanMessage(content=msg)
        result = first_responder_chain.invoke(input={"messages": [human_message]})
        print(result)
