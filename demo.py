#!/usr/bin/env python3
"""
Hivra Network Demo
Demonstrates the core functionality
"""
from cli import CapsuleSystem
from src.core.capsule import CapsuleType

def run_demo():
    print("=== HIVRA NETWORK DEMO ===\n")
    
    system = CapsuleSystem()
    
    # 1. Create capsules
    print("1. Creating capsules...")
    capsule_a = system.create_capsule("capsule_a", CapsuleType.GENESIS)
    capsule_b = system.create_capsule("capsule_b", CapsuleType.PROTO)
    print(f"   Created: {capsule_a.id} ({capsule_a.capsule_type.value})")
    print(f"   Created: {capsule_b.id} ({capsule_b.capsule_type.value})")
    
    # 2. Add starter to capsule A
    print("\n2. Adding starter to capsule A...")
    starter_a_id = system.add_starter_to_capsule("capsule_a")
    print(f"   Starter created: {starter_a_id}")
    
    # 3. Send invitation
    print(f"\n3. Sending invitation from A to B...")
    system.send_invite("capsule_a", "capsule_b", starter_a_id)
    
    # Check status
    status_b = system.get_status("capsule_b")
    invited = status_b["relationships"].get("capsule_a", {}).get("invited", False)
    print(f"   Capsule B invited by A: {invited}")
    
    # 4. Accept invitation
    print("\n4. Capsule B accepts invitation...")
    events = system.accept_invite("capsule_b", "capsule_a", starter_a_id)
    print(f"   Generated events: {len(events)}")
    
    # Check status after acceptance
    status_b = system.get_status("capsule_b")
    occupied_slots = [s for s in status_b['slots'] if s['state'] == 'occupied']
    print(f"   Capsule B has {len(occupied_slots)} occupied slot(s)")
    
    if occupied_slots:
        starter_b_id = occupied_slots[0]['starter_id']
        print(f"   Generated starter: {starter_b_id}")
    
    # 5. Toggle trust
    print("\n5. Toggling trust relationship...")
    system.toggle_trust("capsule_b", "capsule_a")
    
    status_b = system.get_status("capsule_b")
    trusted = status_b["relationships"].get("capsule_a", {}).get("trusted", False)
    print(f"   Capsule B trusts A: {trusted}")
    
    # 6. Final status
    print("\n6. Final status:")
    print("   Capsule A:")
    status_a = system.get_status("capsule_a")
    for slot in status_a["slots"]:
        if slot["state"] == "occupied":
            print(f"     Slot {slot['slot']}: {slot['starter_id']}")
    
    print("\n   Capsule B:")
    for slot in status_b["slots"]:
        if slot["state"] == "occupied":
            print(f"     Slot {slot['slot']}: {slot['starter_id']}")
    
    print("\n   Capsule B relationships:")
    for other, rel in status_b["relationships"].items():
        print(f"     {other}: invited={rel['invited']}, trusted={rel['trusted']}")
    
    print("\n=== DEMO COMPLETE ===")

if __name__ == "__main__":
    run_demo()
