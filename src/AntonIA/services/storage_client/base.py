from pathlib import Path
from typing import Protocol, Optional

from logging import getLogger



logger = getLogger("AntonIA.local_storage_client")


class StorageClient(Protocol):
    def save_file(self, data: bytes, file_path: Path, destination: Optional[list[str]]) -> str:
        """Save a file to the storage and return its URL or identifier."""
        pass


class MockStorageClient:
    def save_file(self, data: bytes, filename: str, destination: Optional[list[str]] = None) -> str:
        logger.info(f"Mock save file '{filename}' to destination '{'/'.join(destination) if destination else ''}'")
        return f"mock://{('/'.join(destination) + '/' if destination else '')}{filename}"
    