from typing import List
from AsteriskRealtimeData.domain.agent.agent_vo import AgentVo
from AsteriskRealtimeData.application.agent_service import AgentService
from AsteriskRealtimeData.domain.agent.agent_update_vo import AgentUpdateVo
from AsteriskRealtimeData.domain.agent.agent_search_criteria_vo import (
    AgentSearchCriteriaVo,
)


class AgentController:
    def create(self, agent_vo: AgentVo) -> AgentVo:
        return AgentService().create_agent(agent_vo)

    def update(self, agent_update_vo: AgentUpdateVo) -> AgentVo:
        return AgentService().update_agent(agent_update_vo)

    def get_all(self) -> List[AgentVo]:
        agents = AgentService().agent_list()
        result: list = []

        for agent in agents:
            result.append(agent)

        return result

    def get_by_agent_loginqad(self, agent_loginqad: str) -> AgentVo:
        return AgentService().get_agent(loginqad=agent_loginqad)

    def get_by_search_criteria(self, search_criteria: AgentSearchCriteriaVo) -> AgentVo:
        return AgentService().get_by_search_criteria(search_criteria)

    def delete_by_agent_loginqad(self, agent_loginqad: str) -> None:
        AgentService().delete_agent(loginqad=agent_loginqad)
