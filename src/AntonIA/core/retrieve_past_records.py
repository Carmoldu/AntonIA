from datetime import datetime
import pandas as pd

from AntonIA.core.prompt_generator import logger
from AntonIA.services.database_client import DatabaseClient


def retrieve_past_n_days(database_client: DatabaseClient, table: str, n_days: int) -> str:
    """
    Retrieves past runs' outputs from the database.
    Args:
        database_client: instance of the DatabaseClient abstraction
        table: name of the table to query
        n_days: number of past days to retrieve
    
    Returns:
        str: Each record as a line starting with a tab
    """
    logger.info(f"Retrieving past {n_days} days outputs from database table '{table}'...")
    query = f"timestamp >= '{(datetime.now() - pd.Timedelta(days=n_days)).date()}'"
    records = database_client.get_records_matching_query(table, query)
    formatted_records = "\n".join("\t" + str(record) for record in records.to_dict(orient="records"))
    return formatted_records
