from typing import TypedDict, List, Dict, Any


class GraphState(TypedDict):
    query: str
    report_name: str
    stages: List[str]
    prompts: Any
    agents: Any
    agent_result: Any
    generation: str
    websearch: bool
    documents: List[str]
