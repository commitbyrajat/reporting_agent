from typing import List, Iterator, Union, Any

from langchain_core.messages import BaseMessage, AIMessage, HumanMessage
from langgraph.constants import END

from agent import master_data_agent, transaction_agent, user_management_agent
from chain import parser_tool


def agent_router(state: List[BaseMessage]) -> str:
    tool_invocation: AIMessage = state[-1]
    parser_tool_calls = parser_tool.invoke(tool_invocation)

    selected_db = parser_tool_calls[-1]["args"]["selected_db"]
    print("Selected DB: ", selected_db)
    if selected_db == "NO_MATCH":
        return END
    return selected_db


def execute_transaction_agent(state: List[BaseMessage]):
    user_query: HumanMessage = state[0]
    events = transaction_agent.stream(
        {"messages": [("user", user_query.content)]},
        {"recursion_limit": 50},
        stream_mode="values",
    )
    return event_iterator(events)


def execute_master_data_agent(state: List[BaseMessage]):
    user_query: HumanMessage = state[0]
    events = master_data_agent.stream(
        {"messages": [("user", user_query.content)]},
        {"recursion_limit": 50},
        stream_mode="values",
    )
    return event_iterator(events)


def execute_user_management_agent(state: List[BaseMessage]):
    user_query: HumanMessage = state[0]
    events = user_management_agent.stream(
        {"messages": [("user", user_query.content)]},
        {"recursion_limit": 50},
        stream_mode="values",
    )
    return event_iterator(events)


def event_iterator(events: Iterator[Union[dict[str, Any], Any]]):
    responses = []
    for event in events:
        event["messages"][-1].pretty_print()
        response = event["messages"][-1].content
        responses.append(response)

    return responses
