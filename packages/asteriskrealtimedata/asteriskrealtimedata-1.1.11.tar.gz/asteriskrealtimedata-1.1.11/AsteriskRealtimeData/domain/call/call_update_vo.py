from AsteriskRealtimeData.domain.update_vo import UpdateVo
from dataclasses import dataclass
from typing import Any


@dataclass
class CallUpdateVo(UpdateVo):
    call_linkedid: str
    peer_name: Any = None
    queue_member_name: Any = None
    client_id: Any = None
    dialnumber: Any = None
    lastevent: Any = None
    track_id: Any = None
    call_actor_address: Any = None
    call_linked: Any = None
    call_transfered: Any = None
    call_status: Any = None
    call_direction: Any = None
    event_name: Any = None
    origin_number: Any = None
    origin_channel: Any = None
    origin_channel_state: Any = None
    origin_channel_state_desc: Any = None
    destination_number: Any = None
    destination_channel: Any = None
    destination_channel_state: Any = None
    destination_channel_state_desc: Any = None
    transfered_number: Any = None
    transfered_channel: Any = None
    transfered_channel_state: Any = None
    transfered_channel_state_desc: Any = None
    hangup_cause: Any = None
    hangup_cause_desc: Any = None
    _update_keys: str = "call_linkedid"

