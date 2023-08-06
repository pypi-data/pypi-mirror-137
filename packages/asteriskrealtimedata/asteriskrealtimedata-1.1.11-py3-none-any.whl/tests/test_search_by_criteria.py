import unittest
from typing import Final

from AsteriskRealtimeData.application.agent_service import AgentService
from AsteriskRealtimeData.domain.agent.agent_search_criteria_vo import (
    AgentSearchCriteriaVo,
)
from AsteriskRealtimeData.domain.mascara_ipaddress.mascara_ipaddress_search_criteria_vo import (
    MascaraIpaddressSearchCriteriaVo,
)
from AsteriskRealtimeData.application.mascara_ipaddress_service import (
    MascaraIpaddressService,
)
from AsteriskRealtimeData.domain.call.call_search_criteria_vo import CallSerchCriteriaVo
from AsteriskRealtimeData.shared.errors.data_not_found_error import DataNotFound


class TestSearchCriteriaVo(unittest.TestCase):
    DATA_NO_FOUND: Final = "Data not found"

    def test_call_search_by_criteria_vo(self):
        search_one_term = CallSerchCriteriaVo(peer_name="SIP/100", origin_channel="123")
        print(search_one_term.as_dict())

    def test_ipaddress_search_by_criteria_vo(self):
        with self.assertRaises(DataNotFound) as context:
            MascaraIpaddressService().get_by_search_criteria(
                MascaraIpaddressSearchCriteriaVo(ipaddress="172.0.0.1")
            )
        self.assertTrue(self.DATA_NO_FOUND in str(context.exception))

    def test_agent_search_by_criteria(self):
        agent = AgentService().get_by_search_criteria(
            AgentSearchCriteriaVo(loginqad="1001")
        )
        print(agent.as_dict())
