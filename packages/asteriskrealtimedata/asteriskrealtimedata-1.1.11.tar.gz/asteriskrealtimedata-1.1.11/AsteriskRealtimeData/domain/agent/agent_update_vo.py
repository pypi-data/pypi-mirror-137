from typing import Any
from dataclasses import dataclass
from AsteriskRealtimeData.domain.update_vo import UpdateVo


@dataclass
class AgentUpdateVo(UpdateVo):
    loginqad: str
    anexo: Any = None
    nombre: Any = None
    actualip: Any = None
    is_tester: Any = None
    _update_keys: str = "loginqad"
