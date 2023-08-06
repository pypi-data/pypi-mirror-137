from datetime import datetime
from dataclasses import dataclass


@dataclass
class CallVo:
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

    def as_dict(self) -> dict:
        return self.__repr__()

    def __repr__(self):
        return {
            "peer_name": self.peer_name,
            "queue_member_name": self.queue_member_name,
            "client_id": self.client_id,
            "dialnumber": self.dialnumber,
            "lastevent": self.lastevent,
            "track_id": self.track_id,
            "call_linkedid": self.call_linkedid,
            "call_actor_address": self.call_actor_address,
            "call_linked": self.call_linked,
            "call_transfered": self.call_transfered,
            "call_status": self.call_status,
            "call_direction": self.call_direction,
            "event_name": self.event_name,
            "origin_number": self.origin_number,
            "origin_channel": self.origin_channel,
            "origin_channel_state": self.origin_channel_state,
            "origin_channel_state_desc": self.origin_channel_state_desc,
            "destination_number": self.destination_number,
            "destination_channel": self.destination_channel,
            "destination_channel_state": self.destination_channel_state,
            "destination_channel_state_desc": self.destination_channel_state_desc,
            "transfered_number": self.transfered_number,
            "transfered_channel": self.transfered_channel,
            "transfered_channel_state": self.transfered_channel_state,
            "transfered_channel_state_desc": self.transfered_channel_state_desc,
            "hangup_cause": self.hangup_cause,
            "hangup_cause_desc": self.hangup_cause_desc,
        }
