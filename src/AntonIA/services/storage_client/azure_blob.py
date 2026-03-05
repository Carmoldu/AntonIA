from pathlib import PurePosixPath

from azure.storage.blob import BlobServiceClient, ContentSettings

import mimetypes
from typing import Optional

from logging import getLogger



logger = getLogger("AntonIA.azure_storage_client")

class AzureBlobStorageClient:
    def __init__(
        self,
        connection_string: str,
        container_name: str,
        base_dir: Optional[str] = None,
    ):
        """
        Initialize Azure Blob Storage client.

        Args:
            connection_string: Azure Storage connection string
            container_name: Name of the blob container
            base_dir (optional): Base directory within the container to save files. Defaults to root.
        """
        self.blob_service_client = BlobServiceClient.from_connection_string(
            connection_string
        )
        self.container_client = self.blob_service_client.get_container_client(
            container_name
        )
        self.container_name = container_name
        self.base_dir = PurePosixPath(base_dir) if base_dir else PurePosixPath()

    def save_file(
        self,
        data: bytes,
        filename: str,
        destination: Optional[list[str]] = None,
    ) -> str:
        """
        Save file bytes to Azure Blob Storage.

        Args:
            data: File content as bytes
            filename: Name of the file
            destination: Optional folder-like path segments

        Returns:
            Blob URL as string
        """
        destination = destination or []

        blob_path = (
            self.base_dir / PurePosixPath(*destination) / filename
        ).as_posix()

        logger.info(f"Uploading blob to '{blob_path}'")

        blob_client = self.container_client.get_blob_client(blob_path)

        blob_client.upload_blob(
            data,
            overwrite=True,
            content_settings=ContentSettings(
                content_type=self._guess_content_type(filename)
            ),
        )

        blob_url = blob_client.url

        logger.info(f"File uploaded to {blob_url}")

        return blob_url

    @staticmethod
    def _guess_content_type(filename: str) -> str:
        content_type, _ = mimetypes.guess_type(filename)
        return content_type or "application/octet-stream"
