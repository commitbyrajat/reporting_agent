import datetime

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import PydanticToolsParser, JsonOutputToolsParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from db import llm
from schema import AnswerQuestion

load_dotenv()


parser_tool = JsonOutputToolsParser(return_id=True)
parser_pydantic = PydanticToolsParser(tools=[AnswerQuestion])

actor_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
     [Timestamp: {timestamp}]

    You are an intelligent database assistant responsible for determining the most relevant database for answering user queries. 
    
    ### **Available Databases:**
    1. **Transaction DB**  
       - Contains tables related to financial transactions and service provider account details.  
       - Use this if the query involves transaction history, payments, service provider-related financial data, or money movement.  
    
    2. **User Management DB**  
       - Contains tables related to user account details.  
       - Use this if the query involves user authentication, account information, or personal financial profiles.  
    
    3. **Master Data DB**  
       - Contains tables with details about all financial instruments.  
       - Use this if the query involves information about mutual funds, stocks, bonds, or any other investment products.
    
    ### **Task:**
    Analyze the following user query and determine the most suitable database(s) to retrieve the required information.
    
    
    ### **Response Format:**
    Provide the name(s) of the most relevant database(s) in a concise format:
    - **Primary Database:** <Best-matching database>
    - **Additional Databases (if applicable):** <Other related databases>
    - **Reasoning:** <Explain why these databases are relevant>
    
    Ensure that the response is accurate, clear, and well-justified.

     """,
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

first_responder_prompt = actor_prompt_template.partial(
    timestamp=lambda: datetime.datetime.now().isoformat()
)
first_responder = first_responder_prompt | llm.bind_tools(
    tools=[AnswerQuestion], tool_choice="AnswerQuestion"
)
first_responder_chain = first_responder | parser_pydantic

if __name__ == "__main__":
    messages = [
        "What all mutual funds are available from HDFC AMC ?",
        "what is the sum of all the transaction values of account number 12345678 ?",
        "what is the PAN card associated with account number 9876543123 ?",
        "How many planets are there in solar system?",
    ]

    for msg in messages:
        print("Query: ", msg)
        human_message = HumanMessage(content=msg)
        result = first_responder_chain.invoke(input={"messages": [human_message]})
        print(result)
