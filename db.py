from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine

# PostgreSQL database connection details
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "localhost"

load_dotenv()
llm = init_chat_model("gpt-4o-mini", model_provider="openai")


def get_engine_by_db(db_name: str, port: int):
    return create_engine(
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{port}/{db_name}"
    )


transaction_engine = get_engine_by_db("transaction", 5432)
master_data_engine = get_engine_by_db("master_data", 5433)
user_management_engine = get_engine_by_db("user_management", 5431)

transaction_db = SQLDatabase(
    transaction_engine, include_tables=["transaction", "service_provider_account"]
)
master_data_db = SQLDatabase(master_data_engine, include_tables=["instrument"])
user_management_db = SQLDatabase(user_management_engine, include_tables=["account"])

transaction_toolkit = SQLDatabaseToolkit(db=transaction_db, llm=llm)
master_data_toolkit = SQLDatabaseToolkit(db=master_data_db, llm=llm)
user_management_toolkit = SQLDatabaseToolkit(db=user_management_db, llm=llm)


all_tools = (
    transaction_toolkit.get_tools()
    + master_data_toolkit.get_tools()
    + user_management_toolkit.get_tools()
)

if __name__ == "__main__":
    print([tool.name for tool in all_tools.values()])
