from typing import Any
from dataclasses import dataclass
from AsteriskRealtimeData.domain.search_by_criteria_vo import SearchByCriteriaVo


@dataclass
class AgentSearchCriteriaVo(SearchByCriteriaVo):
    anexo: Any = None
    nombre: Any = None
    loginqad: Any = None
    actualip: Any = None
    is_tester: Any = None
