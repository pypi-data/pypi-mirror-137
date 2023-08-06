from pydantic import BaseModel


class Ping(BaseModel):
    jitter: float
    latency: float
