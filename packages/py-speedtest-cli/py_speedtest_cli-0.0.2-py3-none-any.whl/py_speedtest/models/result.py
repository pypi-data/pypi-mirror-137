import datetime as dt

from pydantic import BaseModel

from .ping import Ping
from .bandwidth import Bandwidth
from .interface import Interface
from .server import Server
from .hosted_result import HostedResult


class Result(BaseModel):
    timestamp: dt.datetime
    ping: Ping
    download: Bandwidth
    upload: Bandwidth
    packetLoss: int
    isp: str
    interface: Interface
    server: Server
    result: HostedResult
