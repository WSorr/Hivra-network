#!/usr/bin/env python3
print("Testing imports...")
try:
    from src.core.capsule import Capsule, CapsuleType
    print("✓ Capsule imported")
    
    from src.events import Event
    print("✓ Event imported")
    
    from src.core.ledger import Ledger
    print("✓ Ledger imported")
    
    print("\n✅ All imports successful")
except Exception as e:
    print(f"❌ Import error: {e}")
    import traceback
    traceback.print_exc()
