import pytest
from unittest.mock import MagicMock
from AntonIA.core import image_saver

class DummyStorageClient:
    def __init__(self):
        self.saved = {}

    def save_file(self, data, filename):
        self.saved[filename] = data
        return f"/fake/path/{filename}"

def test_file_namer_with_date():
    data = b"test image data"
    filename = image_saver.file_namer(data, extension=".png", add_date=True)
    assert filename.endswith(".png")
    assert len(filename.split("_")) == 3  # date, hash, extension

def test_file_namer_without_date():
    data = b"test image data"
    filename = image_saver.file_namer(data, extension=".png", add_date=False)
    assert filename.endswith(".png")
    assert "_" not in filename[:-4]  # only hash, no date

def test_save_calls_storage_client_and_returns_path():
    data = b"image bytes"
    storage_client = DummyStorageClient()
    result_path = image_saver.save(data, storage_client, add_date=True)
    assert result_path.startswith("/fake/path/")
    # Check that the file was saved
    saved_filename = result_path.split("/")[-1]
    assert storage_client.saved[saved_filename] == data

def test_save_filename_changes_with_add_date():
    data = b"image bytes"
    storage_client = DummyStorageClient()
    path_with_date = image_saver.save(data, storage_client, add_date=True)
    path_without_date = image_saver.save(data, storage_client, add_date=False)
    assert path_with_date != path_without_date