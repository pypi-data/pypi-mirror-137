from pydantic import BaseModel


class Server(BaseModel):
    id: int
    name: str
    location: str
    country: str
    host: str
    port: int
    ip: str
