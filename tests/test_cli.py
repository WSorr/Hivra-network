#!/usr/bin/env python3
"""
Simple CLI test.
"""
import os
import sys
import tempfile
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/../")

from src.core.capsule import Capsule, CapsuleType
from src.core.ledger import Ledger
from src.core.state import State


def test_cli_simulation():
    """Simulate CLI operations programmatically."""
    print("Testing CLI simulation...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        data_dir = Path(tmpdir)
        print(f"Using temp directory: {data_dir}")
        
        # Simulate: capsulenet create proto test-alice
        print("\n1. Creating PROTO capsule 'test-alice'...")
        capsule = Capsule(capsule_id="test-alice", capsule_type=CapsuleType.PROTO)
        ledger = Ledger("test-alice")
        state = State("test-alice", CapsuleType.PROTO)
        
        # Save files like CLI would
        capsule_file = data_dir / "test-alice_capsule.json"
        with open(capsule_file, 'w') as f:
            json.dump(capsule.to_dict(), f, indent=2)
        
        ledger_file = data_dir / "test-alice_ledger.json"
        ledger.save_to_file(str(ledger_file))
        
        state_file = data_dir / "test-alice_state.json"
        with open(state_file, 'w') as f:
            json.dump(state.to_dict(), f, indent=2)
        
        print(f"   ✓ Created: {capsule_file.name}")
        print(f"   ✓ Created: {ledger_file.name}")
        print(f"   ✓ Created: {state_file.name}")
        
        # Simulate: capsulenet create genesis test-bob
        print("\n2. Creating GENESIS capsule 'test-bob'...")
        capsule2 = Capsule(capsule_id="test-bob", capsule_type=CapsuleType.GENESIS)
        ledger2 = Ledger("test-bob")
        state2 = State("test-bob", CapsuleType.GENESIS)
        
        capsule_file2 = data_dir / "test-bob_capsule.json"
        with open(capsule_file2, 'w') as f:
            json.dump(capsule2.to_dict(), f, indent=2)
        
        print(f"   ✓ Created: {capsule_file2.name}")
        
        # Simulate: capsulenet list
        print("\n3. Listing capsules...")
        for file in data_dir.glob("*_capsule.json"):
            capsule_id = file.name.replace("_capsule.json", "")
            print(f"   - {capsule_id}")
        
        # Simulate: capsulenet send test-bob friendship
        print("\n4. Simulating invitation send...")
        slot = capsule2.get_slot("friendship")
        if slot and slot.starter_id:
            print(f"   Would send starter: {slot.starter_id[:8]}...")
            print(f"   From: test-bob (GENESIS)")
            print(f"   To: test-alice (PROTO)")
            print(f"   Slot type: friendship")
            print("   ✓ Invitation simulation complete")
        else:
            print("   ✗ No starter in friendship slot")
        
        # Verify files
        print("\n5. Verifying created files...")
        files = list(data_dir.glob("*.json"))
        print(f"   Found {len(files)} files:")
        for f in files:
            print(f"   - {f.name}")
        
        return len(files) >= 3  # At least 3 files (capsule, ledger, state)


def main():
    """Run CLI tests."""
    print("=" * 60)
    print("CLI Simulation Test")
    print("=" * 60)
    
    try:
        success = test_cli_simulation()
        
        if success:
            print("\n✅ CLI simulation test PASSED")
            return 0
        else:
            print("\n❌ CLI simulation test FAILED")
            return 1
            
    except Exception as e:
        print(f"\n❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
