from typing import List
from antidote import inject, Provide
from AsteriskRealtimeData.domain.call.call_search_criteria_vo import CallSerchCriteriaVo
from AsteriskRealtimeData.domain.call.call_update_vo import CallUpdateVo
from AsteriskRealtimeData.application.call_repository import CallRepository
from AsteriskRealtimeData.domain.call.call import Call
from AsteriskRealtimeData.domain.call.call_vo import CallVo


class CallService:
    @inject
    def create_call(self, call_vo: CallVo, repository: Provide[CallRepository],) -> CallVo:

        call = Call(
            peer_name=call_vo.peer_name,
            queue_member_name=call_vo.queue_member_name,
            client_id=call_vo.client_id,
            dialnumber=call_vo.dialnumber,
            lastevent=call_vo.lastevent,
            track_id=call_vo.track_id,
            call_linkedid=call_vo.call_linkedid,
            call_actor_address=call_vo.call_actor_address,
            call_linked=call_vo.call_linked,
            call_transfered=call_vo.call_transfered,
            call_status=call_vo.call_status,
            call_direction=call_vo.call_direction,
            event_name=call_vo.event_name,
            origin_number=call_vo.origin_number,
            origin_channel=call_vo.origin_channel,
            origin_channel_state=call_vo.origin_channel_state,
            origin_channel_state_desc=call_vo.origin_channel_state_desc,
            destination_number=call_vo.destination_number,
            destination_channel=call_vo.destination_channel,
            destination_channel_state=call_vo.destination_channel_state,
            destination_channel_state_desc=call_vo.destination_channel_state_desc,
            transfered_number=call_vo.transfered_number,
            transfered_channel=call_vo.transfered_channel,
            transfered_channel_state=call_vo.transfered_channel_state,
            transfered_channel_state_desc=call_vo.transfered_channel_state_desc,
            hangup_cause=call_vo.hangup_cause,
            hangup_cause_desc=call_vo.hangup_cause_desc,
        )

        repository.save(call, {"call_linkedid": call_vo.call_linkedid})

        return CallVo(
            peer_name=call_vo.peer_name,
            queue_member_name=call_vo.queue_member_name,
            client_id=call_vo.client_id,
            dialnumber=call_vo.dialnumber,
            lastevent=call_vo.lastevent,
            track_id=call_vo.track_id,
            call_linkedid=call_vo.call_linkedid,
            call_actor_address=call_vo.call_actor_address,
            call_linked=call_vo.call_linked,
            call_transfered=call_vo.call_transfered,
            call_status=call_vo.call_status,
            call_direction=call_vo.call_direction,
            event_name=call_vo.event_name,
            origin_number=call_vo.origin_number,
            origin_channel=call_vo.origin_channel,
            origin_channel_state=call_vo.origin_channel_state,
            origin_channel_state_desc=call_vo.origin_channel_state_desc,
            destination_number=call_vo.destination_number,
            destination_channel=call_vo.destination_channel,
            destination_channel_state=call_vo.destination_channel_state,
            destination_channel_state_desc=call_vo.destination_channel_state_desc,
            transfered_number=call_vo.transfered_number,
            transfered_channel=call_vo.transfered_channel,
            transfered_channel_state=call_vo.transfered_channel_state,
            transfered_channel_state_desc=call_vo.transfered_channel_state_desc,
            hangup_cause=call_vo.hangup_cause,
            hangup_cause_desc=call_vo.hangup_cause_desc,
        )

    @inject
    def update_call(self, call_update_vo: CallUpdateVo, repository: Provide[CallRepository]) -> CallVo:

        repository.update(call_update_vo)

        call_dict = repository.get_by_criteria(call_update_vo.get_key_field())

        return CallVo(
            peer_name=call_dict["peer_name"],
            queue_member_name=call_dict["queue_member_name"],
            client_id=call_dict["client_id"],
            dialnumber=call_dict["dialnumber"],
            lastevent=call_dict["lastevent"],
            track_id=call_dict["track_id"],
            call_linkedid=call_dict["call_linkedid"],
            call_actor_address=call_dict["call_actor_address"],
            call_linked=call_dict["call_linked"],
            call_transfered=call_dict["call_transfered"],
            call_status=call_dict["call_status"],
            call_direction=call_dict["call_direction"],
            event_name=call_dict["event_name"],
            origin_number=call_dict["origin_number"],
            origin_channel=call_dict["origin_channel"],
            origin_channel_state=call_dict["origin_channel_state"],
            origin_channel_state_desc=call_dict["origin_channel_state_desc"],
            destination_number=call_dict["destination_number"],
            destination_channel=call_dict["destination_channel"],
            destination_channel_state=call_dict["destination_channel_state"],
            destination_channel_state_desc=call_dict["destination_channel_state_desc"],
            transfered_number=call_dict["transfered_number"],
            transfered_channel=call_dict["transfered_channel"],
            transfered_channel_state=call_dict["transfered_channel_state"],
            transfered_channel_state_desc=call_dict["transfered_channel_state_desc"],
            hangup_cause=call_dict["hangup_cause"],
            hangup_cause_desc=call_dict["hangup_cause_desc"],
        )

    @inject()
    def call_list(self, repository: Provide[CallRepository]) -> List[CallVo]:
        result: list = []
        for document in repository.list():
            result.append(
                CallVo(
                    peer_name=document["peer_name"],
                    queue_member_name=document["queue_member_name"],
                    client_id=document["client_id"],
                    dialnumber=document["dialnumber"],
                    lastevent=document["lastevent"],
                    track_id=document["track_id"],
                    call_linkedid=document["call_linkedid"],
                    call_actor_address=document["call_actor_address"],
                    call_linked=document["call_linked"],
                    call_transfered=document["call_transfered"],
                    call_status=document["call_status"],
                    call_direction=document["call_direction"],
                    event_name=document["event_name"],
                    origin_number=document["origin_number"],
                    origin_channel=document["origin_channel"],
                    origin_channel_state=document["origin_channel_state"],
                    origin_channel_state_desc=document["origin_channel_state_desc"],
                    destination_number=document["destination_number"],
                    destination_channel=document["destination_channel"],
                    destination_channel_state=document["destination_channel_state"],
                    destination_channel_state_desc=document["destination_channel_state_desc"],
                    transfered_number=document["transfered_number"],
                    transfered_channel=document["transfered_channel"],
                    transfered_channel_state=document["transfered_channel_state"],
                    transfered_channel_state_desc=document["transfered_channel_state_desc"],
                    hangup_cause=document["hangup_cause"],
                    hangup_cause_desc=document["hangup_cause_desc"],
                )
            )
        return result

    @inject
    def get_call(self, call_linkedid: str, repository: Provide[CallRepository]) -> CallVo:

        call = repository.get_by_criteria({"call_linkedid": call_linkedid})
        return CallVo(
            peer_name=call["peer_name"],
            queue_member_name=call["queue_member_name"],
            client_id=call["client_id"],
            dialnumber=call["dialnumber"],
            lastevent=call["lastevent"],
            track_id=call["track_id"],
            call_linkedid=call["call_linkedid"],
            call_actor_address=call["call_actor_address"],
            call_linked=call["call_linked"],
            call_transfered=call["call_transfered"],
            call_status=call["call_status"],
            call_direction=call["call_direction"],
            event_name=call["event_name"],
            origin_number=call["origin_number"],
            origin_channel=call["origin_channel"],
            origin_channel_state=call["origin_channel_state"],
            origin_channel_state_desc=call["origin_channel_state_desc"],
            destination_number=call["destination_number"],
            destination_channel=call["destination_channel"],
            destination_channel_state=call["destination_channel_state"],
            destination_channel_state_desc=call["destination_channel_state_desc"],
            transfered_number=call["transfered_number"],
            transfered_channel=call["transfered_channel"],
            transfered_channel_state=call["transfered_channel_state"],
            transfered_channel_state_desc=call["transfered_channel_state_desc"],
            hangup_cause=call["hangup_cause"],
            hangup_cause_desc=call["hangup_cause_desc"],
        )

    @inject
    def get_by_search_criteria(
        self, search_criteria: CallSerchCriteriaVo, repository: Provide[CallRepository]
    ) -> CallVo:
        call = repository.get_by_criteria(search_criteria.as_dict())
        return CallVo(
            peer_name=call["peer_name"],
            queue_member_name=call["queue_member_name"],
            client_id=call["client_id"],
            dialnumber=call["dialnumber"],
            lastevent=call["lastevent"],
            track_id=call["track_id"],
            call_linkedid=call["call_linkedid"],
            call_actor_address=call["call_actor_address"],
            call_linked=call["call_linked"],
            call_transfered=call["call_transfered"],
            call_status=call["call_status"],
            call_direction=call["call_direction"],
            event_name=call["event_name"],
            origin_number=call["origin_number"],
            origin_channel=call["origin_channel"],
            origin_channel_state=call["origin_channel_state"],
            origin_channel_state_desc=call["origin_channel_state_desc"],
            destination_number=call["destination_number"],
            destination_channel=call["destination_channel"],
            destination_channel_state=call["destination_channel_state"],
            destination_channel_state_desc=call["destination_channel_state_desc"],
            transfered_number=call["transfered_number"],
            transfered_channel=call["transfered_channel"],
            transfered_channel_state=call["transfered_channel_state"],
            transfered_channel_state_desc=call["transfered_channel_state_desc"],
            hangup_cause=call["hangup_cause"],
            hangup_cause_desc=call["hangup_cause_desc"],
        )

    @inject
    def delete_call(self, call_linkedid: str, repository: Provide[CallRepository]) -> None:
        repository.delete_by_criteria({"call_linkedid": call_linkedid})
