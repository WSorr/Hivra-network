#!/usr/bin/env python3
"""
Test new event system.
"""
import sys

print("Testing new event system...")

try:
    # Test importing from new system
    from src.events import Event, InvitationEvent
    
    print("✓ Imported Event and InvitationEvent")
    
    # Create simple event
    event = Event(event_type="test_event")
    print(f"✓ Created Event: {event.event_type}")
    print(f"  Event ID: {event.event_id}")
    print(f"  Timestamp: {event.timestamp}")
    
    # Create invitation event
    invite = InvitationEvent(
        invitation_id="test_invite_001",
        sender_id="alice",
        recipient_id="bob",
        starter_id="starter_123",
        capsule_id="alice",
        slot_type="friendship"
    )
    print(f"\n✓ Created InvitationEvent: {invite.event_type}")
    print(f"  Sender: {invite.sender_id}")
    print(f"  Recipient: {invite.recipient_id}")
    print(f"  Starter: {invite.starter_id[:10]}...")
    
    # Test serialization
    event_dict = event.to_dict()
    print(f"\n✓ Event serialized to dict")
    print(f"  Dict keys: {list(event_dict.keys())}")
    
    # Test deserialization
    event_from_dict = Event.from_dict(event_dict)
    print(f"✓ Event deserialized from dict")
    print(f"  Same type: {event_from_dict.event_type == event.event_type}")
    
    # Test JSON
    event_json = event.to_json()
    print(f"\n✓ Event serialized to JSON")
    print(f"  JSON length: {len(event_json)} chars")
    
    event_from_json = Event.from_json(event_json)
    print(f"✓ Event deserialized from JSON")
    print(f"  Same event ID: {event_from_json.event_id == event.event_id}")
    
    print("\n✅ New event system works!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
