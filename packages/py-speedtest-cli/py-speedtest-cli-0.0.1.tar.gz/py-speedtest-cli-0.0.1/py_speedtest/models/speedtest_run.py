from pydantic import BaseModel, Field

from .result import Result
from .log_entry import LogEntry


class SpeedtestRun(BaseModel):
    result: Result = None
    logs: list[LogEntry] = Field(default_factory=list)
