import json
import pandas as pd
from langchain_core.tools import tool


@tool
def convert_json_to_csv(json_input: str) -> str:
    """Convert JSON data to CSV and return the CSV content as a string."""
    try:
        data = json.loads(json_input)
        df = pd.DataFrame(data)
        csv_output = df.to_csv(index=False)
        return csv_output
    except Exception as e:
        return str(e)
