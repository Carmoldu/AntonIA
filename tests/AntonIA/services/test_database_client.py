import pytest
import pandas as pd
from AntonIA.services.database_client import MockDatabaseClient, LocalFileDatabaseClient

def test_mock_save_and_get_all_records():
    client = MockDatabaseClient()
    table = "users"
    record1 = {"id": 1, "name": "Alice"}
    record2 = {"id": 2, "name": "Bob"}

    client.save_record(table, record1)
    client.save_record(table, record2)

    df = client.get_all_records(table)
    assert len(df) == 2
    assert set(df["name"]) == {"Alice", "Bob"}

def test_mock_get_records_matching_query():
    client = MockDatabaseClient()
    table = "users"
    client.save_record(table, {"id": 1, "name": "Alice", "age": 30})
    client.save_record(table, {"id": 2, "name": "Bob", "age": 25})

    df = client.get_records_matching_query(table, "age > 28")
    assert len(df) == 1
    assert df.iloc[0]["name"] == "Alice"

def test_mock_get_all_records_empty_table():
    client = MockDatabaseClient()
    df = client.get_all_records("nonexistent")
    assert isinstance(df, pd.DataFrame)
    assert df.empty

def test_mock_get_records_matching_query_invalid_query():
    client = MockDatabaseClient()
    table = "users"
    client.save_record(table, {"id": 1, "name": "Alice"})
    df = client.get_records_matching_query(table, "unknown_column == 1")
    assert df.empty

def test_local_file_save_and_get_all_records(tmp_path):
    client = LocalFileDatabaseClient(str(tmp_path))
    table = "products"
    record1 = {"id": 1, "name": "Widget"}
    record2 = {"id": 2, "name": "Gadget"}

    client.save_record(table, record1)
    client.save_record(table, record2)

    df = client.get_all_records(table)
    assert len(df) == 2
    assert set(df["name"]) == {"Widget", "Gadget"}

def test_local_file_get_all_records_empty_table(tmp_path):
    client = LocalFileDatabaseClient(str(tmp_path))
    df = client.get_all_records("nonexistent")
    assert isinstance(df, pd.DataFrame)
    assert df.empty

def test_local_file_get_records_matching_query(tmp_path):
    client = LocalFileDatabaseClient(str(tmp_path))
    table = "users"
    client.save_record(table, {"id": 1, "name": "Alice", "age": 30})
    client.save_record(table, {"id": 2, "name": "Bob", "age": 25})

    df = client.get_records_matching_query(table, "age < 28")
    assert len(df) == 1
    assert df.iloc[0]["name"] == "Bob"

def test_local_file_get_records_matching_query_invalid(tmp_path):
    client = LocalFileDatabaseClient(str(tmp_path))
    table = "users"
    client.save_record(table, {"id": 1, "name": "Alice"})
    with pytest.raises(Exception):
        client.get_records_matching_query(table, "unknown_column == 1")