from pathlib import Path
from logging import getLogger
from typing import Protocol, Optional



logger = getLogger("AntonIA.storage_client")

class StorageClient(Protocol):
    def save_file(self, file_path: Path, destination: str) -> str:
        """Save a file to the storage and return its URL or identifier."""
        pass


class LocalStorageClient:
    def __init__(self, base_dir: str):
        """
        Initialize the local storage client.

        Args:
            base_dir: local directory where files will be saved
        """
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def save_file(self, data: bytes, filename: str, destination: Optional[list[str]] = None) -> str:
        """
        Save a file to the local storage.

        Args:
            file_path: path to the file to be saved
            destination: relative path within the storage base directory

        Returns:
            Full path to the saved file as a string
        """
        dest_path = self.base_dir / (Path(*destination) if destination else Path()) / filename
        dest_path.parent.mkdir(parents=True, exist_ok=True)

        with open(dest_path, "wb") as f:
            f.write(data)

        logger.info(f"File saved to {dest_path}")
        return str(dest_path)
    
