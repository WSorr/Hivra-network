#!/usr/bin/env python3
"""
Simple demo without complex imports.
"""
import sys

print("Simple Hivra V1 Demo")
print("=" * 50)

try:
    # Import only what we need
    from src.core.capsule import Capsule, CapsuleType
    from src.core.ledger import Ledger
    from src.core.state import State
    from src.events.base import Event
    
    print("✓ Imports successful")
    
    # Create capsules
    print("\n1. Creating capsules:")
    proto = Capsule(capsule_id="demo-proto", capsule_type=CapsuleType.PROTO)
    genesis = Capsule(capsule_id="demo-genesis", capsule_type=CapsuleType.GENESIS)
    
    print(f"   PROTO: {proto.capsule_id}")
    print(f"     - Slots: {len(proto.slots)}")
    print(f"     - Empty slots: {sum(1 for s in proto.slots.values() if not s.starter_id)}")
    
    print(f"\n   GENESIS: {genesis.capsule_id}")
    print(f"     - Slots: {len(genesis.slots)}")
    print(f"     - Starters: {sum(1 for s in genesis.slots.values() if s.starter_id)}")
    
    # Create ledger
    print("\n2. Creating ledger:")
    ledger = Ledger("demo-ledger")
    event = Event(event_type="demo_event")
    ledger.append(event)
    
    print(f"   Ledger entries: {len(ledger.entries)}")
    print(f"   Last sequence: {ledger._sequence_counter}")
    
    # Create state
    print("\n3. Creating state:")
    state = State("demo-state", CapsuleType.PROTO)
    new_state = state.apply_event(event)
    
    print(f"   Initial sequence: {state._sequence}")
    print(f"   After event: {new_state._sequence}")
    
    # Test binary starter concept
    print("\n4. Binary starter concept:")
    print("   Starter is an abstract ON/OFF switch")
    print("   Initial: OFF")
    print("   Sent with invitation: ON")
    print("   Connection cancelled: OFF")
    print("   Controlled by events, not directly by user")
    
    print("\n✅ V1 Demo successful!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
