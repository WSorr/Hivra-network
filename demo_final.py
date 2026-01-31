#!/usr/bin/env python3
"""
Hivra CapsuleNet V1 - Final Demo
"""
print("=" * 60)
print("Hivra CapsuleNet V1")
print("=" * 60)

from src.core.capsule import Capsule, CapsuleType
from src.events import Event, create_invitation_event
from src.core.ledger import Ledger

print("\n1. Creating capsules with proper starter names:")
print("   Starter types: ⚡ Juice, 💥 Spark, 🌱 Seed, 📡 Pulse, 🔥 Kick")

proto = Capsule(capsule_id="alice", capsule_type=CapsuleType.PROTO)
print(f"\n   PROTO: {proto.capsule_id}")
print("   Slots (all empty):")
for slot_name in proto.slots:
    print(f"     - {slot_name}")

genesis = Capsule(capsule_id="bob", capsule_type=CapsuleType.GENESIS)
print(f"\n   GENESIS: {genesis.capsule_id}")
print("   Slots (all have starters):")
for slot_name, slot in genesis.slots.items():
    if slot.starter_id:
        print(f"     - {slot_name}: {slot.starter_id[:12]}...")

print("\n2. Sending invitation:")
juice_starter = genesis.get_starter_id("⚡ Juice")
if juice_starter:
    invite = create_invitation_event(
        invitation_id="inv_001",
        sender_id="bob",
        recipient_id="alice",
        starter_id=juice_starter,
        capsule_id="bob",
        slot_type="⚡ Juice"
    )
    print(f"   Event: {invite.event_type}")
    print(f"   From: {invite.metadata.get('sender_id')}")
    print(f"   To: {invite.metadata.get('recipient_id')}")
    print(f"   Starter: {invite.metadata.get('starter_id')[:12]}...")
    print(f"   Slot: {invite.metadata.get('slot_type')}")

print("\n3. V1 Architecture Summary:")
print("   ✓ Ledger: Append-only event log")
print("   ✓ State: Immutable, deterministic")
print("   ✓ Starters: Binary switches (⚡💥🌱📡🔥)")
print("   ✓ Events: All state changes via events")
print("   ✓ Genesis: Auto-created starters")
print("   ✓ PROTO: Empty slots, needs invitation")

print("\n" + "=" * 60)
print("✅ V1 Ready!")
print("=" * 60)
