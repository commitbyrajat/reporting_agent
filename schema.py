from typing import List

from pydantic import BaseModel, Field


class ReportIdentifier(BaseModel):
    """Identify the type of report and its corresponding sequence of stages"""

    report_name: str = Field(
        description=(
            "Identifies the most relevant report based on the query. "
            "Must return one of the following predefined report names if a match is found: \n"
            "- 'NET_SALES': Contains sequence of stages for generating the net sales report.\n"
            "- 'TRANSACTION_SUMMARY': Used for summarizing transactions.\n"
            "- 'USER_ACTIVITY': Tracks user account activity.\n"
            "- 'NO_MATCH': If no suitable match is found.\n"
        ),
        examples=["NET_SALES", "TRANSACTION_SUMMARY", "USER_ACTIVITY", "NO_MATCH"],
    )

    stages: List[str] = Field(
        description=(
            "Defines the sequence of stages required for generating the report. "
            "Each stage represents a database or a processing step required.\n"
            "For example:\n"
            "- 'NET_SALES' -> ['TRANSACTION_DB', 'MASTER_DATA_DB', 'USER_MANAGEMENT_DB']\n"
            "- 'TRANSACTION_SUMMARY' -> ['TRANSACTION_DB']\n"
            "- 'USER_ACTIVITY' -> ['USER_MANAGEMENT_DB']\n"
        ),
        examples=[
            ["TRANSACTION_DB", "MASTER_DATA_DB", "USER_MANAGEMENT_DB"],
            ["TRANSACTION_DB"],
            ["USER_MANAGEMENT_DB"],
        ],
    )


class AnswerQuestion(BaseModel):
    """Answer the Question"""

    selected_db: str = Field(
        description=(
            "Identifies the most relevant database for the given query. "
            "Must return one of the following predefined database names if a match is found: \n"
            "- 'TRANSACTION_DB': Contains transaction records and service provider account details.\n"
            "- 'USER_MANAGEMENT_DB': Stores user account details.\n"
            "- 'MASTER_DATA_DB': Holds information about financial instruments such as mutual funds, stocks, and bonds.\n"
            "- 'NO_MATCH': If no suitable match is found.\n"
        ),
        examples=["TRANSACTION_DB", "USER_MANAGEMENT_DB", "MASTER_DATA_DB", "NO_MATCH"],
    )
