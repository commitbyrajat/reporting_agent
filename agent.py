from dotenv import load_dotenv
from langchain import hub
from langgraph.prebuilt import create_react_agent

from db import llm, transaction_toolkit, master_data_toolkit, user_management_toolkit

load_dotenv()

# Load system prompt
prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")
system_message = prompt_template.format(dialect="PostgreSQL", top_k=5)

# Create separate agents for each database
transaction_agent = create_react_agent(
    llm, tools=transaction_toolkit.get_tools(), prompt=system_message
)
master_data_agent = create_react_agent(
    llm, tools=master_data_toolkit.get_tools(), prompt=system_message
)
user_management_agent = create_react_agent(
    llm, tools=user_management_toolkit.get_tools(), prompt=system_message
)
