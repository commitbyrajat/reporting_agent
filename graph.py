from dotenv import load_dotenv
from langgraph.graph import MessageGraph

from chain import first_responder
from nodes import (
    agent_router,
    execute_master_data_agent,
    execute_user_management_agent,
    execute_transaction_agent,
)

load_dotenv()
graph = MessageGraph()
graph.add_node("first_responder", first_responder)
graph.set_entry_point("first_responder")

graph.add_conditional_edges("first_responder", agent_router)

graph.add_node("MASTER_DATA_DB", execute_master_data_agent)
graph.add_node("USER_MANAGEMENT_DB", execute_user_management_agent)
graph.add_node("TRANSACTION_DB", execute_transaction_agent)


graph = graph.compile()
print(graph.get_graph().draw_ascii())

if __name__ == "__main__":
    messages = [
        "What all mutual funds are available from HDFC AMC ?",
        "what is the name in user's account where bos code is 900492549?",
    ]

    for msg in messages:
        result = graph.invoke(msg)
        print("======================================================================")
        print(result[-1].content)
