#!/usr/bin/env python3
print("=" * 60)
print("Hivra CapsuleNet V1 - Working Demo")
print("=" * 60)

from src.core.capsule import Capsule, CapsuleType
from src.events import Event, create_invitation_event
from src.core.ledger import Ledger
from src.core.state import State

print("\n1. Creating capsules:")
proto = Capsule(capsule_id="alice-proto", capsule_type=CapsuleType.PROTO)
print(f"   PROTO: {proto.capsule_id}")
print(f"     Slots: {len(proto.slots)} (all empty)")

genesis = Capsule(capsule_id="bob-genesis", capsule_type=CapsuleType.GENESIS)
print(f"\n   GENESIS: {genesis.capsule_id}")
print(f"     Slots: {len(genesis.slots)} (all have starters)")

print("\n2. Creating events:")
event1 = Event(event_type="capsule_created")
print(f"   Event 1: {event1.event_type}")

friendship_starter = genesis.get_starter_id("friendship")
if friendship_starter:
    event2 = create_invitation_event(
        invitation_id="inv_001",
        sender_id="bob-genesis",
        recipient_id="alice-proto",
        starter_id=friendship_starter,
        capsule_id="bob-genesis",
        slot_type="friendship"
    )
    print(f"   Event 2: {event2.event_type}")
    print(f"     Sender: {event2.metadata.get('sender_id')}")
    print(f"     Starter: {event2.metadata.get('starter_id')[:12]}...")

print("\n3. Using ledger:")
ledger = Ledger("demo-ledger")
entry1 = ledger.append(event1, tags=["creation"])
print(f"   Added event 1, sequence: {entry1.sequence_number}")

if friendship_starter:
    entry2 = ledger.append(event2, tags=["invitation"])
    print(f"   Added event 2, sequence: {entry2.sequence_number}")

print(f"\n   Total entries: {len(ledger.entries)}")

print("\n4. Using state:")
state = State("demo-state", CapsuleType.PROTO)
print(f"   Initial sequence: {state._sequence}")

new_state = state.apply_event(event1)
print(f"   After event, new sequence: {new_state._sequence}")

print("\n" + "=" * 60)
print("✅ V1 Core Components Working!")
print("=" * 60)
