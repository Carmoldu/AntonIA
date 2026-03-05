from typing import Protocol, Optional



class StorageClient(Protocol):
    def save_file(self, data: bytes, filename: str, destination: Optional[list[str]] = None) -> str:
        """Save a file to the storage and return its URL or identifier."""
        ...
    