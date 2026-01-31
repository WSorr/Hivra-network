"""
Tests for Ledger and State.
"""
import pytest
import tempfile
import os
from datetime import datetime

from src.core.ledger import Ledger, LedgerEntry
from src.core.state import State, CapsuleType
from src.events.base import Event
from src.events.actions import GenerateEvent


class TestEvent(Event):
    """Test event for testing."""
    def __init__(self, test_data: str):
        super().__init__(event_type="test")
        self.test_data = test_data


def test_ledger_creation():
    """Test ledger initialization."""
    ledger = Ledger("test_capsule")
    assert ledger.capsule_id == "test_capsule"
    assert len(ledger.entries) == 0
    assert ledger._sequence_counter == 0


def test_ledger_append():
    """Test appending events to ledger."""
    ledger = Ledger("test_capsule")
    event = TestEvent("test_data")
    
    entry = ledger.append(event, tags=["test"])
    
    assert len(ledger.entries) == 1
    assert entry.event == event
    assert entry.sequence_number == 1
    assert entry.tags == ["test"]
    assert entry.capsule_id == "test_capsule"


def test_ledger_get_entries():
    """Test retrieving entries with filters."""
    ledger = Ledger("test_capsule")
    
    event1 = TestEvent("data1")
    event2 = TestEvent("data2")
    
    ledger.append(event1, tags=["tag1"])
    ledger.append(event2, tags=["tag2"])
    
    # Get all entries
    all_entries = ledger.get_entries()
    assert len(all_entries) == 2
    
    # Get entries by tag
    tag1_entries = ledger.get_entries(tags=["tag1"])
    assert len(tag1_entries) == 1
    assert tag1_entries[0].event == event1
    
    # Get entries with multiple tags
    multi_entries = ledger.get_entries(tags=["tag1", "tag2"])
    assert len(multi_entries) == 2


def test_ledger_serialization():
    """Test ledger serialization/deserialization."""
    ledger = Ledger("test_capsule")
    event = TestEvent("test_data")
    ledger.append(event, tags=["test"])
    
    # Convert to dict and back
    ledger_dict = ledger.to_dict()
    restored_ledger = Ledger.from_dict(ledger_dict)
    
    assert restored_ledger.capsule_id == ledger.capsule_id
    assert len(restored_ledger.entries) == len(ledger.entries)
    assert restored_ledger._sequence_counter == ledger._sequence_counter
    
    # Compare entries
    original_entry = ledger.entries[0]
    restored_entry = restored_ledger.entries[0]
    assert original_entry.id == restored_entry.id
    assert original_entry.event.event_type == restored_entry.event.event_type


def test_ledger_file_io():
    """Test saving/loading ledger to/from file."""
    ledger = Ledger("test_capsule")
    event = TestEvent("test_data")
    ledger.append(event, tags=["test"])
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_path = f.name
    
    try:
        # Save ledger
        ledger.save_to_file(temp_path)
        assert os.path.exists(temp_path)
        
        # Load ledger
        loaded_ledger = Ledger.load_from_file(temp_path)
        
        assert loaded_ledger.capsule_id == ledger.capsule_id
        assert len(loaded_ledger.entries) == len(ledger.entries)
        
    finally:
        # Cleanup
        if os.path.exists(temp_path):
            os.unlink(temp_path)


def test_state_initialization():
    """Test state initialization based on capsule type."""
    # Test PROTO capsule
    proto_state = State("proto_capsule", CapsuleType.PROTO)
    assert proto_state.capsule_id == "proto_capsule"
    assert proto_state.capsule_type == CapsuleType.PROTO
    
    # All slots should be empty for PROTO
    for slot_type in ["friendship", "collaboration", "trust", "exchange", "alliance"]:
        assert proto_state.is_slot_empty(slot_type)
        assert proto_state.get_slot(slot_type) is None
    
    # Test GENESIS capsule (slots will be populated by mechanics, not initialization)
    genesis_state = State("genesis_capsule", CapsuleType.GENESIS)
    assert genesis_state.capsule_type == CapsuleType.GENESIS


def test_state_immutability():
    """Test that state is never modified in place."""
    state = State("test_capsule", CapsuleType.PROTO)
    event = TestEvent("test")
    
    # Apply event should return NEW state
    new_state = state.apply_event(event)
    
    # Original state should be unchanged
    assert state is not new_state
    assert state._sequence == 0
    assert new_state._sequence == 1


def test_state_serialization():
    """Test state serialization/deserialization."""
    state = State("test_capsule", CapsuleType.PROTO)
    
    # Convert to dict and back
    state_dict = state.to_dict()
    restored_state = State.from_dict(state_dict)
    
    assert restored_state.capsule_id == state.capsule_id
    assert restored_state.capsule_type == state.capsule_type
    assert restored_state._sequence == state._sequence
    
    # Compare slots
    for slot_type in state._slots:
        assert restored_state.get_slot(slot_type) == state.get_slot(slot_type)


def test_state_get_active_starters():
    """Test getting active starters."""
    state = State("test_capsule", CapsuleType.PROTO)
    
    # Initially no active starters
    active = state.get_active_starters()
    assert len(active) == 0
    
    # Note: Adding starters would require event mechanics to be implemented


def test_state_connections():
    """Test connection management."""
    state = State("test_capsule", CapsuleType.PROTO)
    
    # Initially no connections
    connections = state.get_connections()
    assert len(connections) == 0
    
    # Test with specific status
    from src.core.state import ConnectionStatus
    pending = state.get_connections(ConnectionStatus.PENDING)
    assert len(pending) == 0


if __name__ == "__main__":
    pytest.main([__file__])
