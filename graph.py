from dotenv import load_dotenv
from langgraph.graph import StateGraph

from chain import gaurd_rail
from nodes import (
    report_router,
    execute_net_sales_agent,
    first_responder_node,
    execute_sql_agent,
)
from state import GraphState

load_dotenv()
graph = StateGraph(GraphState)
graph.add_node("first_responder", first_responder_node)
graph.set_entry_point("first_responder")


graph.add_conditional_edges(
    "first_responder", report_router, {"NET_SALES": "NET_SALES"}
)

graph.add_node("NET_SALES", execute_net_sales_agent)
graph.add_node("SQL_AGENT", execute_sql_agent)
graph.add_edge("NET_SALES", "SQL_AGENT")


graph = graph.compile()
print(graph.get_graph().draw_ascii())

if __name__ == "__main__":

    messages = [
        "Generate net sales report.",
        # "what is the name in user's account where bos code is 900492549?",
    ]

    for msg in messages:
        query = gaurd_rail.format(msg)
        result = graph.invoke(input={"query": query})
        print(
            "==================================Graph Output===================================="
        )
        response = result["agent_result"]
        print(response)
