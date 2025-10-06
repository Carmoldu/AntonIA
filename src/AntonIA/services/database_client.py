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

    def get_all_records(self, table: str) -> pd.DataFrame:
        """Retrieve all records from the specified table in the database."""
        pass

    def get_records_matching_query(self, table: str, query: str) -> pd.DataFrame:
        """Retrieve records matching a specific query from the specified table in the database."""
        pass

class MockDatabaseClient:
    """
    Mock client to simulate database operations in memory.
    Useful for testing pipelines without writing to disk.
    """
    def __init__(self):
        self.tables = {}
        self.saved_records = 0

    def save_record(self, table: str, record: dict) -> None:
        if table not in self.tables:
            self.tables[table] = []
        self.tables[table].append(record)
        self.saved_records += 1
        logger.debug(f"[MOCK] Record saved to '{table}' (total: {len(self.tables[table])})")

    def get_all_records(self, table: str) -> pd.DataFrame:
        if table in self.tables:
            return pd.DataFrame(self.tables[table])
        else:
            logger.debug(f"[MOCK] Table '{table}' does not exist.")
            return pd.DataFrame()  # Return empty DataFrame if table doesn't exist
        
    def get_records_matching_query(self, table: str, query: str) -> pd.DataFrame:
        df = self.get_all_records(table)
        if df.empty:
            return df
        try:
            filtered_df = df.query(query)
            return filtered_df
        except Exception as e:
            logger.error(f"[MOCK] Error querying table '{table}': {e}")
            return pd.DataFrame()  # Return empty DataFrame on error


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

    def get_all_records(self, table: str) -> pd.DataFrame:
        """Retrieve all records from the specified table."""
        try:
            df = self.pd.read_parquet(f"{self.db_path}/{table}.parquet")
            return df
        except FileNotFoundError:
            logger.warning(f"Table '{table}' does not exist.")
            return self.pd.DataFrame()  # Return empty DataFrame if table doesn't exist
        
    def get_records_matching_query(self, table: str, query: str) -> pd.DataFrame:
        """Retrieve records matching a specific query from the specified table."""
        df = self.get_all_records(table)
        if df.empty:
            return df
        try:
            filtered_df = df.query(query)
            return filtered_df
        except Exception as e:
            logger.error(f"Error querying table '{table}': {e}")
            raise Exception(f"Error querying table '{table}': {e}") from e
