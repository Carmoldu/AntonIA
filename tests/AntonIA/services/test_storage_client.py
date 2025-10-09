import pytest
import tempfile
import shutil
from pathlib import Path
from AntonIA.services.storage_client import MockStorageClient, LocalStorageClient

def test_mock_storage_client_save_file():
    client = MockStorageClient()
    data = b"test data"
    filename = "test.txt"
    destination = ["folder1", "folder2"]
    url = client.save_file(data, filename, destination)
    assert url == "mock://folder1/folder2/test.txt"

    url_no_dest = client.save_file(data, filename)
    assert url_no_dest == "mock://test.txt"

def test_local_storage_client_save_file_creates_file_and_dirs():
    with tempfile.TemporaryDirectory() as tmpdir:
        client = LocalStorageClient(tmpdir)
        data = b"hello world"
        filename = "file.txt"
        destination = ["subdir1", "subdir2"]

        result_path = client.save_file(data, filename, destination)
        expected_path = Path(tmpdir) / "subdir1" / "subdir2" / filename
        assert result_path == str(expected_path)
        assert expected_path.exists()
        with open(expected_path, "rb") as f:
            assert f.read() == data

def test_local_storage_client_save_file_no_destination():
    with tempfile.TemporaryDirectory() as tmpdir:
        client = LocalStorageClient(tmpdir)
        data = b"abc"
        filename = "file2.txt"

        result_path = client.save_file(data, filename)
        expected_path = Path(tmpdir) / filename
        assert result_path == str(expected_path)
        assert expected_path.exists()
        with open(expected_path, "rb") as f:
            assert f.read() == data

def test_local_storage_client_creates_base_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        base_dir = Path(tmpdir) / "new_base"
        client = LocalStorageClient(str(base_dir))
        assert base_dir.exists()
        assert base_dir.is_dir()