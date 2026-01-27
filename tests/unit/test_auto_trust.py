import pytest
from src.core.capsule import Capsule, CapsuleType
from src.events.base import *
from src.modules.invitation import InvitationModule
from src.modules.trust import TrustModule

def test_auto_trust_on_starter_generation():
    """Test that trust is automatically established when starter is generated from invitation"""
    capsule_b = Capsule(id="b", capsule_type=CapsuleType.PROTO)
    inv_module = InvitationModule(capsule_b)
    trust_module = TrustModule(capsule_b)
    
    # 1. Get invitation
    invite = InviteEvent(
        source="a",
        sender_capsule_id="a",
        target_capsule_id="b",
        sender_starter_id="starter_a1"
    )
    inv_module.handle_event(invite)
    
    assert capsule_b.get_relationship("a").invited == True
    assert capsule_b.get_relationship("a").trusted == False
    
    # 2. Accept invitation (generates starter)
    accept = UserActionEvent(
        source="b",
        action_type=UserActionType.ACCEPT_INVITE,
        target_capsule_id="a",
        invite_sender_id="a",
        invite_starter_id="starter_a1"
    )
    
    result = inv_module.handle_event(accept)
    assert len(result) == 1
    assert isinstance(result[0], StarterEvent)
    assert result[0].metadata["action"] == "starter_generated"
    
    # 3. Process starter event for auto-trust
    trust_module.handle_event(result[0])
    
    assert capsule_b.get_relationship("a").invited == False
    assert capsule_b.get_relationship("a").trusted == True  # Auto-trust established
    
    # 4. Check slot 0 is occupied
    assert capsule_b.slots[0].state == "occupied"
    assert capsule_b.slots[0].starter_id is not None
    
def test_no_auto_trust_without_invitation():
    """Test that starter generation without invitation doesn't auto-trust"""
    capsule = Capsule(id="test", capsule_type=CapsuleType.PROTO)
    trust_module = TrustModule(capsule)
    
    # Starter event NOT from invitation
    starter_event = StarterEvent(
        starter_id="some_starter",
        source="other_capsule",
        metadata={"action": "starter_generated"}  # No 'from_invitation' flag
    )
    
    trust_module.handle_event(starter_event)
    assert capsule.get_relationship("other_capsule").trusted == False
