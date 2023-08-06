from typing import List
from antidote import inject, Provide
from AsteriskRealtimeData.domain.agent.agent import Agent
from AsteriskRealtimeData.domain.agent.agent_vo import AgentVo
from AsteriskRealtimeData.domain.agent.agent_update_vo import AgentUpdateVo
from AsteriskRealtimeData.domain.agent.agent_search_criteria_vo import (
    AgentSearchCriteriaVo,
)
from AsteriskRealtimeData.application.agent_repository import AgentRepository


class AgentService:
    @inject
    def create_agent(
        self, agent_vo: AgentVo, repository: Provide[AgentRepository],
    ) -> AgentVo:

        agent = Agent(
            anexo=agent_vo.anexo,
            nombre=agent_vo.nombre,
            loginqad=agent_vo.loginqad,
            actualip=agent_vo.actualip,
            is_tester=agent_vo.is_tester,
        )

        repository.save(agent, {"loginqad": agent_vo.loginqad})

        return AgentVo(
            anexo=agent_vo.anexo,
            nombre=agent_vo.nombre,
            loginqad=agent_vo.loginqad,
            actualip=agent_vo.actualip,
            is_tester=agent_vo.is_tester,
        )

    @inject
    def update_agent(
        self, agent_update_vo: AgentUpdateVo, repository: Provide[AgentRepository]
    ) -> AgentVo:

        repository.update(agent_update_vo)

        agent_dict = repository.get_by_criteria(agent_update_vo.get_key_field())

        return AgentVo(
            anexo=agent_dict["anexo"],
            nombre=agent_dict["nombre"],
            loginqad=agent_dict["loginqad"],
            actualip=agent_dict["actualip"],
            is_tester=agent_dict["is_tester"],
        )

    @inject()
    def agent_list(self, repository: Provide[AgentRepository]) -> List[AgentVo]:
        result: list = []
        for document in repository.list():
            result.append(
                AgentVo(
                    anexo=document["anexo"],
                    nombre=document["nombre"],
                    loginqad=document["loginqad"],
                    actualip=document["actualip"],
                    is_tester=document["is_tester"],
                )
            )
        return result

    @inject
    def get_agent(self, loginqad: str, repository: Provide[AgentRepository]) -> AgentVo:
        agent = repository.get_by_criteria({"loginqad": loginqad})
        return AgentVo(
            anexo=agent["anexo"],
            nombre=agent["nombre"],
            loginqad=agent["loginqad"],
            actualip=agent["actualip"],
            is_tester=agent["is_tester"],
        )

    @inject
    def get_by_search_criteria(
        self,
        search_criteria: AgentSearchCriteriaVo,
        repository: Provide[AgentRepository],
    ) -> AgentVo:
        agent = repository.get_by_criteria(search_criteria.as_dict())
        return AgentVo(
            anexo=agent["anexo"],
            nombre=agent["nombre"],
            loginqad=agent["loginqad"],
            actualip=agent["actualip"],
            is_tester=agent["is_tester"],
        )

    @inject
    def delete_agent(self, loginqad: str, repository: Provide[AgentRepository]) -> None:
        repository.delete_by_criteria({"loginqad": loginqad})
