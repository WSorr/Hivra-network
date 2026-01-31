#!/usr/bin/env python3
"""
Test imports after fixing dataclass issues.
"""
import sys

print("Testing imports after dataclass fixes...")

try:
    # Test core imports
    from src.core.capsule import Capsule, CapsuleType
    print("✓ src.core.capsule")
    
    from src.core.ledger import Ledger
    print("✓ src.core.ledger")
    
    from src.core.state import State
    print("✓ src.core.state")
    
    # Test event imports
    from src.events.base import Event, StarterEvent, InvitationEvent
    print("✓ src.events.base")
    
    from src.events.invitation import InvitationAcceptedEvent
    print("✓ src.events.invitation")
    
    from src.events.link_intent import LinkIntent
    print("✓ src.events.link_intent")
    
    from src.events.confirm import ConfirmAccept
    print("✓ src.events.confirm")
    
    from src.events.actions import BurnEvent
    print("✓ src.events.actions")
    
    # Test creating instances
    print("\nTesting instance creation...")
    
    # Create base event
    event = Event(event_type="test")
    print(f"✓ Created Event: {event.event_type}")
    
    # Create invitation event
    invite = InvitationEvent(
        invitation_id="test_invite",
        sender_id="alice",
        recipient_id="bob", 
        starter_id="starter_123",
        capsule_id="alice",
        slot_type="friendship"
    )
    print(f"✓ Created InvitationEvent: {invite.event_type}")
    
    # Create capsule
    capsule = Capsule(capsule_id="test", capsule_type=CapsuleType.PROTO)
    print(f"✓ Created Capsule: {capsule.capsule_id}")
    
    print("\n✅ All imports and creations successful!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
