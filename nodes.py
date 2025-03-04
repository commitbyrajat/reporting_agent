import json
from typing import List, Iterator, Union, Any, Dict

from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.constants import END

from agent import (
    master_data_agent,
    transaction_agent,
    user_management_agent,
    json_to_csv_agent,
)
from chain import first_responder_chain, gaurd_rail
from db import llm
from glossary import get_formatting_prompt_by_report_name
from schema import ReportIdentifier
from state import GraphState


def first_responder_node(state: GraphState) -> Dict[str, Any]:
    query = state["query"]
    metadata: ReportIdentifier = first_responder_chain.invoke(
        input={"messages": [HumanMessage(content=query)]}
    )
    return {"report_name": metadata[-1].report_name, "stages": metadata[-1].stages}


def report_router(state: GraphState) -> str:
    print("Selected Report: ", state["report_name"])
    if state["report_name"] == "NO_MATCH":
        return END
    return state["report_name"]


def execute_net_sales_agent(state: GraphState) -> Dict[str, Any]:
    prompts = {
        "TRANSACTION_DB": """
        service_provider_account table has one to many relation with transaction table. transaction table has fk_id_service_provider_account that joins it with service_provider_account table.
        fetch all the transactions matching with service provider account table where cas_feed_unique_hash is null and is_active is True and status is 3 and broker_type not in ("EXT", "ISA") or broker_type is null. 
        Include required columns in result [fk_id_account,fk_id_instrument,account_number, created_date (YYYY-MM-DD), transaction_date (YYYY-MM-DD), order_date (YYYY-MM-DD), total_amount, fk_id_transaction_type, quantity, rm_referral_code, bos_code].
        """,
        "MASTER_DATA_DB": """
        ### **Task Overview**
        You are an intelligent assistant responsible for processing structured JSON data. Your task includes:
        1. Extracting all **unique** `fk_id_instrument` values from the given transaction JSON.
        2. Query the **instrument** table to retrieve only the columns id, fk_id_product, full_name, fk_id_instrument_category, and fundoo_rta_code, ensuring that the primary key (`id`) matches the `fk_id_instrument` values from the provided transaction JSON.
        3. Converting the query result into JSON.
        4. **Merging instrument’s details into its corresponding transaction JSON under the key `"instrument_details"`.**
        5. Returning the final response **strictly as a valid JSON array** of merged transaction objects.
        6. Do **not** wrap the response inside ```json … ```. Return **only** a valid JSON string.
        
        ---
        
        ### **Step 1: Input Transaction JSON**
        The input transaction data follows this format:
        ```json
        {}
        """,
        "USER_MANAGEMENT_DB": """
        ### **Task Overview**
        You are an intelligent assistant responsible for processing structured JSON data. Your task includes:
        
        1. Extracting all **unique** `fk_id_account` values from the given JSON.
        2. Query the **account** table to retrieve only the columns id and "uniqueId", ensuring that the primary key (`id`) matches the `fk_id_account` values from the provided JSON.
        3. Converting the query result into JSON.
        4. **Merging account's details into its corresponding transaction JSON under the key `"account_details"`.**
        5. Returning the final response **strictly as a valid JSON array** of merged transaction objects.
        6. Do **not** wrap the response inside ```json … ```. Return **only** a valid JSON string.

        ---
        
        ### **Step 1: Input Transaction JSON**
        The input transaction data follows this format:
        ```json
        {}
        """,
    }
    agents = {
        "TRANSACTION_DB": transaction_agent,
        "MASTER_DATA_DB": master_data_agent,
        "USER_MANAGEMENT_DB": user_management_agent,
    }

    return {"prompts": prompts, "agents": agents}


def execute_sql_agent(state: GraphState) -> Dict[str, Any]:
    result = {}
    for stage in state["stages"]:
        prompt: str = state["prompts"][stage]
        prompt = prompt.format(result)
        agent = state["agents"][stage]
        events = agent.stream(
            {"messages": [("user", gaurd_rail.format(prompt))]},
            stream_mode="values",
        )
        for event in events:
            event["messages"][-1].pretty_print()

        result = json.loads(event["messages"][-1].content)

    return {"agent_result": result}


def execute_data_formatting_agent(state: GraphState) -> dict[str, Any]:
    report_name = state["report_name"]
    agent_result = state["agent_result"]
    prompt = get_formatting_prompt_by_report_name(report_name, agent_result)
    result = llm.invoke(prompt)
    return {"agent_result": json.loads(result.content)}


def execute_json_to_csv_node(state: GraphState) -> dict[str, Any]:
    agent_result = state["agent_result"]
    query = f"""
    Convert the following JSON data into CSV format. Output only the CSV content without any additional text, explanations, formatting, or surrounding characters like triple backticks:

    `{json.dumps(agent_result)}`
    """
    events = json_to_csv_agent.stream(
        {"messages": [("user", query)]}, stream_mode="values"
    )
    for event in events:
        event["messages"][-1].pretty_print()

    return {"agent_result": event["messages"][-1].content}


# Obsolete - code | but may be required in future
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
