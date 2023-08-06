from pydantic import BaseModel


class Interface(BaseModel):
    internalIp: str
    name: str
    macAddr: str
    isVpn: bool
    externalIp: str
