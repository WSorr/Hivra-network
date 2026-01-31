#!/usr/bin/env python3
"""
Simple import test.
"""
import sys

print("Testing simple imports...")

# Test core imports first
try:
    from src.core.capsule import Capsule, CapsuleType
    print("✓ src.core.capsule")
except Exception as e:
    print(f"✗ src.core.capsule: {e}")

try:
    from src.core.ledger import Ledger
    print("✓ src.core.ledger")
except Exception as e:
    print(f"✗ src.core.ledger: {e}")

try:
    from src.core.state import State
    print("✓ src.core.state")
except Exception as e:
    print(f"✗ src.core.state: {e}")

# Test event imports
print("\nTesting event imports...")

try:
    from src.events.base import Event
    print("✓ src.events.base - Event")
    
    # Try creating an event
    event = Event(event_type="test")
    print(f"  Created Event: {event.event_type}")
except Exception as e:
    print(f"✗ src.events.base: {e}")

try:
    from src.events.base import StarterEvent
    print("✓ src.events.base - StarterEvent")
    
    # Try creating a starter event
    starter_event = StarterEvent(
        starter_id="test_starter",
        capsule_id="test_capsule",
        event_type="starter"
    )
    print(f"  Created StarterEvent: {starter_event.event_type}")
except Exception as e:
    print(f"✗ src.events.base - StarterEvent: {e}")

try:
    from src.events.base import InvitationEvent
    print("✓ src.events.base - InvitationEvent")
    
    # Try creating an invitation event
    invite = InvitationEvent(
        invitation_id="test_invite",
        sender_id="alice",
        recipient_id="bob",
        starter_id="starter_123",
        capsule_id="alice",
        slot_type="friendship"
    )
    print(f"  Created InvitationEvent: {invite.event_type}")
except Exception as e:
    print(f"✗ src.events.base - InvitationEvent: {e}")

print("\n✅ Import test complete")
