import pytest
from AntonIA.services.storage_client import MockStorageClient


def test_mock_storage_client_save_file():
    client = MockStorageClient()
    data = b"test data"
    filename = "test.txt"
    destination = ["folder1", "folder2"]
    url = client.save_file(data, filename, destination)
    assert url == "mock://folder1/folder2/test.txt"

    url_no_dest = client.save_file(data, filename)
    assert url_no_dest == "mock://test.txt"
