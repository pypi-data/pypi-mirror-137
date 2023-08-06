from datetime import datetime
from dataclasses import dataclass
from typing import List
from AsteriskRealtimeData.domain.entity import Entity


@dataclass
class Call(Entity):
    peer_name: str
    queue_member_name: str
    client_id: str
    dialnumber: str
    lastevent: datetime
    track_id: str
    call_linkedid: str
    call_actor_address: str
    call_linked: str
    call_transfered: str
    call_status: str
    call_direction: str
    event_name: str
    origin_number: str
    origin_channel: str
    origin_channel_state: str
    origin_channel_state_desc: str
    destination_number: str
    destination_channel: str
    destination_channel_state: str
    destination_channel_state_desc: str
    transfered_number: str
    transfered_channel: str
    transfered_channel_state: str
    transfered_channel_state_desc: str
    hangup_cause: str
    hangup_cause_desc: str

    def get_peer_name(self) -> str:
        return self.peer_name

    def get_queue_member_name(self) -> str:
        return self.queue_member_name

    def get_client_id(self) -> str:
        return self.client_id

    def get_dialnumber(self) -> str:
        return self.dialnumber

    def get_lastevent(self) -> datetime:
        return self.lastevent

    def get_track_id(self) -> str:
        return self.track_id

    def get_call_linkedid(self) -> str:
        return self.call_linkedid

    def get_call_actor_address(self) -> str:
        return self.call_actor_address

    def get_call_linked(self) -> str:
        return self.call_linked

    def get_call_transfered(self) -> str:
        return self.call_transfered

    def get_call_status(self) -> str:
        return self.call_status

    def get_call_direction(self) -> str:
        return self.call_direction

    def get_event_name(self) -> str:
        return self.event_name

    def get_origin_number(self) -> str:
        return self.origin_number

    def get_origin_channel(self) -> str:
        return self.origin_channel

    def get_origin_channel_state(self) -> str:
        return self.origin_channel_state

    def get_origin_channel_state_desc(self) -> str:
        return self.origin_channel_state_desc

    def get_destination_number(self) -> str:
        return self.destination_number

    def get_destination_channel(self) -> str:
        return self.destination_channel

    def get_destination_channel_state(self) -> str:
        return self.destination_channel_state

    def get_destination_channel_state_desc(self) -> str:
        return self.destination_channel_state_desc

    def get_transfered_number(self) -> str:
        return self.transfered_number

    def get_transfered_channel(self) -> str:
        return self.transfered_channel

    def get_transfered_channel_state(self) -> str:
        return self.transfered_channel_state

    def get_transfered_channel_state_desc(self) -> str:
        return self.transfered_channel_state_desc

    def get_hangup_cause(self) -> str:
        return self.hangup_cause

    def get_hangup_cause_desc(self) -> str:
        return self.hangup_cause_desc

    def as_dict(self) -> dict:
        return self.__repr__()

    def __repr__(self):
        return {
            "id": self.get_id(),
            "peer_name": self.get_peer_name(),
            "queue_member_name": self.get_queue_member_name(),
            "client_id": self.get_client_id(),
            "dialnumber": self.get_dialnumber(),
            "lastevent": self.get_lastevent(),
            "track_id": self.get_track_id(),
            "call_linkedid": self.get_call_linkedid(),
            "call_actor_address": self.get_call_actor_address(),
            "call_linked": self.get_call_linked(),
            "call_transfered": self.get_call_transfered(),
            "call_status": self.get_call_status(),
            "call_direction": self.get_call_direction(),
            "event_name": self.get_event_name(),
            "origin_number": self.get_origin_number(),
            "origin_channel": self.get_origin_channel(),
            "origin_channel_state": self.get_origin_channel_state(),
            "origin_channel_state_desc": self.get_origin_channel_state_desc(),
            "destination_number": self.get_destination_number(),
            "destination_channel": self.get_destination_channel(),
            "destination_channel_state": self.get_destination_channel_state(),
            "destination_channel_state_desc": self.get_destination_channel_state_desc(),
            "transfered_number": self.get_transfered_number(),
            "transfered_channel": self.get_transfered_channel(),
            "transfered_channel_state": self.get_transfered_channel_state(),
            "transfered_channel_state_desc": self.get_transfered_channel_state_desc(),
            "hangup_cause": self.get_hangup_cause(),
            "hangup_cause_desc": self.get_hangup_cause_desc(),
        }

