import os
from typing import Protocol
from logging import getLogger
from pathlib import Path

import pandas as pd



logger = getLogger("AntonIA.database_client")


class DatabaseClient(Protocol):
    def save_record(self, table: str, record: dict) -> None:
        """Save a record to the specified table in the database."""
        pass


class LocalFileDatabaseClient:
    def __init__(self, db_path: str):
        # Generate the database directory if it doesn't exist
        db_path = Path(db_path)
        db_path.mkdir(parents=True, exist_ok=True)

        self.db_path = db_path
        self.pd = pd

    def save_record(self, table: str, record: dict) -> None:
        """Save a record to a parquet file representing the table."""
        new_row = self.pd.DataFrame([record])

        try:
            df = self.pd.read_parquet(f"{self.db_path}/{table}.parquet")
            df = self.pd.concat([df, new_row], ignore_index=True)
        except FileNotFoundError:
            df = self.pd.DataFrame([record])
        
        df.to_parquet(f"{self.db_path}/{table}.parquet", index=False)
        logger.info(f"Record saved to {table} table.")
