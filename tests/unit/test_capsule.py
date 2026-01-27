import pytest
from src.core.capsule import Capsule, CapsuleType

def test_capsule_creation():
    capsule = Capsule(id="test", capsule_type=CapsuleType.PROTO)
    assert capsule.id == "test"
    assert capsule.capsule_type == CapsuleType.PROTO
    assert len(capsule.slots) == 5

def test_capsule_has_empty_slot():
    capsule = Capsule(id="test", capsule_type=CapsuleType.PROTO)
    assert capsule.has_empty_slot() == True
    
    for i in range(5):
        capsule.slots[i].state = "occupied"
    assert capsule.has_empty_slot() == False

def test_capsule_relationship_management():
    capsule = Capsule(id="a", capsule_type=CapsuleType.PROTO)
    rel = capsule.get_relationship("b")
    assert rel.invited == False
    
    rel.invited = True
    assert capsule.get_relationship("b").invited == True
