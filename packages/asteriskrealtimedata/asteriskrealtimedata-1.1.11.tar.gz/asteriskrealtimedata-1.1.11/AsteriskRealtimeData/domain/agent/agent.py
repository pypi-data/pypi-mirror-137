from dataclasses import dataclass
from ipaddress import IPv4Address
from AsteriskRealtimeData.domain.entity import Entity


@dataclass
class Agent(Entity):
    anexo: str
    nombre: str
    loginqad: str
    actualip: IPv4Address
    is_tester: bool

    def get_anexo(self) -> str:
        return self.anexo

    def get_nombre(self) -> str:
        return self.nombre

    def get_loginqad(self) -> str:
        return self.loginqad

    def get_actualip(self) -> IPv4Address:
        return self.actualip

    def get_is_tester(self) -> bool:
        return self.is_tester

    def as_dict(self) -> dict:
        return self.__repr__()

    def __repr__(self):
        return {
            "id": self.get_id(),
            "anexo": self.get_anexo(),
            "nombre": self.get_nombre(),
            "loginqad": self.get_loginqad(),
            "actualip": self.get_actualip(),
            "is_tester": self.get_is_tester(),
        }
