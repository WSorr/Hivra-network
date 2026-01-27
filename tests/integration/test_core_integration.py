import pytest
from src.core.capsule import Capsule, CapsuleType
from src.core.starter import Starter
from src.events.base import *
from src.coordinator.event_bus import EventBus
from src.modules.invitation import InvitationModule
from src.modules.trust import TrustModule

class TestIntegration:
    def test_full_flow(self):
        capsule_a = Capsule(id="a", capsule_type=CapsuleType.GENESIS)
        capsule_b = Capsule(id="b", capsule_type=CapsuleType.PROTO)
        
        inv_module_a = InvitationModule(capsule_a)
        inv_module_b = InvitationModule(capsule_b)
        trust_module_b = TrustModule(capsule_b)
        
        bus = EventBus()
        bus.subscribe(InviteEvent, inv_module_a.handle_event)
        bus.subscribe(InviteEvent, inv_module_b.handle_event)
        bus.subscribe(UserActionEvent, inv_module_a.handle_event)
        bus.subscribe(UserActionEvent, inv_module_b.handle_event)
        bus.subscribe(UserActionEvent, trust_module_b.handle_event)
        bus.subscribe(StarterEvent, trust_module_b.handle_event)
        
        # 1. A invites B
        invite = InviteEvent(
            source="a",
            sender_capsule_id="a",
            target_capsule_id="b",
            sender_starter_id="starter_a1"
        )
        bus.publish(invite)
        
        assert capsule_b.get_relationship("a").invited == True
        assert capsule_b.get_relationship("a").trusted == False
        
        # 2. B accepts invitation
        accept = UserActionEvent(
            source="b",
            action_type=UserActionType.ACCEPT_INVITE,
            target_capsule_id="a",
            invite_sender_id="a",
            invite_starter_id="starter_a1"
        )
        
        new_events = bus.publish(accept)
        assert len(new_events) == 1
        
        # Process generated StarterEvent for auto-trust
        for event in new_events:
            bus.publish(event)
        
        assert capsule_b.get_relationship("a").invited == False
        assert capsule_b.get_relationship("a").trusted == True  # Auto-trust should be established
        
        # 3. Check that slot 0 is occupied
        assert capsule_b.slots[0].state == "occupied"
        assert capsule_b.slots[0].starter_id is not None
        
        # 4. B toggles trust manually (should turn it OFF)
        toggle = UserActionEvent(
            source="b",
            action_type=UserActionType.TOGGLE_STATE,
            target_capsule_id="a",
            state_name="trusted"
        )
        
        bus.publish(toggle)
        assert capsule_b.get_relationship("a").trusted == False  # Toggled OFF
        
        # 5. Toggle again (should turn ON)
        bus.publish(toggle)
        assert capsule_b.get_relationship("a").trusted == True  # Toggled ON
