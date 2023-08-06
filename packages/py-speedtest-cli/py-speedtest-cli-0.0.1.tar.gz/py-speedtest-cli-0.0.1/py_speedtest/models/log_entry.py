import datetime as dt

from pydantic import BaseModel


class LogEntry(BaseModel):
    timestamp: dt.datetime
    message: str
    level: str

    @property
    def is_error(self) -> bool:
        return self.level.lower() == "error"
