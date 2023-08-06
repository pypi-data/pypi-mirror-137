from dataclasses import dataclass
from ipaddress import IPv4Address


@dataclass
class AgentVo:
    anexo: str
    nombre: str
    loginqad: str
    actualip: IPv4Address
    is_tester: bool

    def as_dict(self) -> dict:
        return self.__repr__()

    def __repr__(self):
        return {
            "anexo": self.anexo,
            "nombre": self.nombre,
            "loginqad": self.loginqad,
            "actualip": self.actualip,
            "is_tester": self.is_tester,
        }
