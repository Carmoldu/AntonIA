from datetime import datetime
from logging import getLogger
import hashlib
from ..services.storage_client import LocalStorageClient



logger = getLogger("AntonIA.image_saver")

def file_namer(data: bytes, extension: str, add_date: bool = True) -> str:
    hash_digest = hashlib.sha256(data).hexdigest()[:8]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") if add_date else ""
    parts = [part for part in [timestamp, hash_digest] if part]
    return "_".join(parts) + extension

def save(image_data: bytes, storage_client: LocalStorageClient, add_date: bool = True) -> str:
    """
    Save image data using the provided storage client.

    Args:
        image_data: binary image data to be saved
        storage_client: instance of LocalStorageClient to handle saving
        add_date: whether to include the current date in the filename

    Returns:
        Path to the saved image file as a string
    """
    logger.info("Saving image...")
    filename = file_namer(image_data, extension=".png", add_date=add_date)
    return storage_client.save_file(image_data, filename)

