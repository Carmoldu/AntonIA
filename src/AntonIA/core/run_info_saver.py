from dataclasses import dataclass, field, asdict
from typing import Any
from datetime import datetime
from logging import getLogger

from ..services.database_client import DatabaseClient



logger = getLogger("AntonIA.run_info_saver")

def _utcnow_iso() -> datetime:
    return datetime.now()

@dataclass
class RunInfo:
    timestamp: datetime = field(default_factory=_utcnow_iso)
    prompt: str
    phrase: str
    topic: str
    style: str
    caption: str
    image_path: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_generation_details(
            prompt: str,
            response_details: dict[str, str],
            caption: str,
            image_path: str,
        ) -> "RunInfo":
        return RunInfo(
            prompt=prompt,
            phrase=response_details["phrase"],
            topic=response_details["topic"],
            style=response_details["style"],
            caption=caption,
            image_path=image_path,
        )


def save(db_client: DatabaseClient, table: str, record: RunInfo) -> None:
    """
    Save run information to the database.

    Args:
        db_client: instance of DatabaseClient to handle saving
        table: name of the table where the record will be saved
        record: dictionary containing the run information to save
    """
    logger.info("Saving run information to the database...")
    db_client.save_record(table, record.as_dict())
    logger.info("Run information saved successfully.")
