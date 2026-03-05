from typing import Optional
from logging import getLogger



logger = getLogger("AntonIA.mock_storage_client")

class MockStorageClient:
    def save_file(self, data: bytes, filename: str, destination: Optional[list[str]] = None) -> str:
        destination = destination or []
        
        logger.info(f"Mock save file '{filename}' to destination '{'/'.join(destination) if destination else ''}'")

        path = "/".join(destination + [filename])
        return f"mock://{path}"
    