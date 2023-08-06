from pydantic import BaseModel


class Bandwidth(BaseModel):
    bandwidth: int
    bytes: int
    elapsed: int
