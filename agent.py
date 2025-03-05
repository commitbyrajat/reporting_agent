from dotenv import load_dotenv
from langchain import hub
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

from db import llm, transaction_toolkit, master_data_toolkit, user_management_toolkit
from tools import convert_json_to_csv

load_dotenv()

# Load system prompt
prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")
system_message = prompt_template.format(dialect="PostgreSQL", top_k=5)
memory = MemorySaver()
# Create separate agents for each database
transaction_agent = create_react_agent(
    llm,
    tools=transaction_toolkit.get_tools(),
    name="TRANSACTION_DB",
    prompt=system_message,
    checkpointer=memory,
)
master_data_agent = create_react_agent(
    llm,
    tools=master_data_toolkit.get_tools(),
    name="MASTER_DATA_DB",
    prompt=system_message,
    checkpointer=memory,
)
user_management_agent = create_react_agent(
    llm,
    tools=user_management_toolkit.get_tools(),
    name="USER_MANAGEMENT_DB",
    prompt=system_message,
    checkpointer=memory,
)

json_to_csv_agent = create_react_agent(
    llm,
    tools=[convert_json_to_csv],
)
