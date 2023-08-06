from pydantic import BaseModel


class HostedResult(BaseModel):
    id: str
    url: str
