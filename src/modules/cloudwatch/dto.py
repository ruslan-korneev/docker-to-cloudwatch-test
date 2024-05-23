from pydantic import Field, RootModel

from src.core.dto import BaseDTO
from src.core.utils import utcnow


def default_timestamp() -> int:
    """Returns the current timestamp in milliseconds"""
    return int(utcnow().timestamp() * 1000)


class LogEvent(BaseDTO):
    timestamp: int = Field(
        default_factory=default_timestamp,
        description="Timestamp in milliseconds",
    )
    message: str


class LogEvents(RootModel[list[LogEvent]]): ...
