import pytest
import pandas as pd
from unittest.mock import MagicMock, patch
from AntonIA.core.retrieve_past_records import retrieve_past_n_days

class DummyDatabaseClient:
    def get_records_matching_query(self, table, query):
        # Simulate returning a DataFrame with some records
        data = [
            {"id": 1, "timestamp": "2024-06-10", "output": "result1"},
            {"id": 2, "timestamp": "2024-06-11", "output": "result2"},
        ]
        return pd.DataFrame(data)

@patch("AntonIA.core.retrieve_past_records.logger")
def test_retrieve_past_n_days_returns_formatted_records(mock_logger):
    db_client = DummyDatabaseClient()
    table = "test_table"
    n_days = 2

    result = retrieve_past_n_days(db_client, table, n_days)
    # Each record should be a line starting with a tab
    lines = result.split("\n")
    assert all(line.startswith("\t") for line in lines)
    assert "result1" in result
    assert "result2" in result
    mock_logger.info.assert_called_once()

@patch("AntonIA.core.retrieve_past_records.logger")
def test_retrieve_past_n_days_empty_records(mock_logger):
    class EmptyDatabaseClient:
        def get_records_matching_query(self, table, query):
            return pd.DataFrame([])

    db_client = EmptyDatabaseClient()
    table = "test_table"
    n_days = 2

    result = retrieve_past_n_days(db_client, table, n_days)
    assert result == ""
    mock_logger.info.assert_called_once()