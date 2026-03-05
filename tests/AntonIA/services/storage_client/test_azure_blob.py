import pytest
from AntonIA.services.storage_client import AzureBlobStorageClient


def test_azure_blob_storage_client_save_file(monkeypatch):
    # Prepare dummy Azure SDK objects to avoid network calls
    dummy_service = None

    class DummyBlobClient:
        def __init__(self):
            self.uploaded_data = None
            self.overwrite = None
            self.content_type = None
            self.url = "https://fake.blob.core.windows.net/container/blob"

        def upload_blob(self, data, overwrite, content_settings):
            self.uploaded_data = data
            self.overwrite = overwrite
            # content_settings is a ContentSettings object
            self.content_type = content_settings.content_type

    class DummyContainer:
        def __init__(self):
            self.blob_client = DummyBlobClient()
            self.last_path = None

        def get_blob_client(self, path):
            self.last_path = path
            return self.blob_client

    class DummyService:
        def __init__(self):
            self.container = DummyContainer()
            self.conn_str = None

        def get_container_client(self, container_name):
            self.container_name = container_name
            return self.container

    dummy_service = DummyService()

    def fake_from_connection_string(conn_str):
        dummy_service.conn_str = conn_str
        return dummy_service

    # Patch the Azure SDK constructor
    monkeypatch.setattr(
        "AntonIA.services.storage_client.azure_blob.BlobServiceClient.from_connection_string",
        fake_from_connection_string,
    )

    # Create the client and call save_file
    client = AzureBlobStorageClient(
        connection_string="conn+string",
        container_name="mycontainer",
        base_dir="base/path",
    )

    data = b"abc123"
    filename = "image.png"
    destination = ["folder1", "folder2"]

    returned_url = client.save_file(data, filename, destination)

    # Validate that the Azure client was used as expected
    assert dummy_service.conn_str == "conn+string"
    assert dummy_service.container_name == "mycontainer"
    assert dummy_service.container.last_path == "base/path/folder1/folder2/image.png"

    blob_client = dummy_service.container.blob_client
    assert blob_client.uploaded_data == data
    assert blob_client.overwrite is True
    assert blob_client.content_type == "image/png"
    assert returned_url == blob_client.url


def test_guess_content_type():
    # known type
    assert AzureBlobStorageClient._guess_content_type("file.html") == "text/html"
    # unknown extension falls back to octet-stream
    assert AzureBlobStorageClient._guess_content_type("file.unknownext") == "application/octet-stream"
