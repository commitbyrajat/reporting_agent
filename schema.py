from pydantic import BaseModel, Field


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
