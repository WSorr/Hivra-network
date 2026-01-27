import pytest
from src.events.base import *

def test_event_creation():
    event = Event(source="test")
    assert event.source == "test"
    assert hasattr(event, 'id')
    assert hasattr(event, 'timestamp')

def test_starter_event():
    event = StarterEvent(starter_id="s123", source="capsule_a")
    assert event.starter_id == "s123"
    assert event.source == "capsule_a"

def test_invite_event():
    event = InviteEvent(
        source="a",
        sender_capsule_id="a",
        target_capsule_id="b",
        sender_starter_id="s1"
    )
    assert event.sender_capsule_id == "a"
    assert event.target_capsule_id == "b"

def test_user_action_event():
    event = UserActionEvent(
        source="user",
        action_type=UserActionType.ACCEPT_INVITE,
        target_capsule_id="capsule_123"
    )
    assert event.action_type == UserActionType.ACCEPT_INVITE
    assert event.target_capsule_id == "capsule_123"
