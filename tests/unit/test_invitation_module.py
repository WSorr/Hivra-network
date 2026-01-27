import pytest
from src.core.capsule import Capsule, CapsuleType
from src.events.base import *
from src.modules.invitation import InvitationModule

def test_invite_reception():
    capsule = Capsule(id="b", capsule_type=CapsuleType.PROTO)
    module = InvitationModule(capsule)
    
    event = InviteEvent(
        source="a",
        sender_capsule_id="a",
        target_capsule_id="b",
        sender_starter_id="s1"
    )
    
    module.handle_event(event)
    assert capsule.get_relationship("a").invited == True

def test_accept_invite_with_empty_slot():
    capsule = Capsule(id="b", capsule_type=CapsuleType.PROTO)
    module = InvitationModule(capsule)
    
    invite = InviteEvent(
        source="a",
        sender_capsule_id="a",
        target_capsule_id="b",
        sender_starter_id="s1"
    )
    module.handle_event(invite)
    assert capsule.get_relationship("a").invited == True
    
    accept = UserActionEvent(
        source="b",
        action_type=UserActionType.ACCEPT_INVITE,
        target_capsule_id="a",
        invite_sender_id="a",
        invite_starter_id="s1"
    )
    
    result = module.handle_event(accept)
    assert capsule.get_relationship("a").invited == False
    assert len(result) == 1
    assert isinstance(result[0], StarterEvent)
    assert result[0].metadata["action"] == "starter_generated"

def test_reject_invite_with_empty_slot():
    capsule = Capsule(id="b", capsule_type=CapsuleType.PROTO)
    module = InvitationModule(capsule)
    
    invite = InviteEvent(
        source="a",
        sender_capsule_id="a",
        target_capsule_id="b",
        sender_starter_id="s1"
    )
    module.handle_event(invite)
    
    reject = UserActionEvent(
        source="b",
        action_type=UserActionType.REJECT_INVITE,
        target_capsule_id="a",
        invite_sender_id="a",
        invite_starter_id="s1"
    )
    
    result = module.handle_event(reject)
    assert capsule.get_relationship("a").invited == False
    assert len(result) == 1
    assert result[0].metadata["action"] == "starter_burned"
