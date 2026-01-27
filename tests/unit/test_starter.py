import pytest
from src.core.starter import Starter

def test_starter_generation():
    starter = Starter.generate("capsule_123")
    assert starter.owner_capsule_id == "capsule_123"
    assert len(starter.id) == 36
