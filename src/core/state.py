"""
Immutable State - simplified version.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple
from enum import Enum

from src.core.capsule import Capsule, Slot, Starter, CapsuleType
from src.events import Event  # Fixed import


class ConnectionStatus(Enum):
    PENDING = "pending"
    ACTIVE = "active"
    REJECTED = "rejected"
    BURNED = "burned"


@dataclass(frozen=True)
class Connection:
    connection_id: str
    capsule_a_id: str
    capsule_b_id: str
    starter_type: str
    status: ConnectionStatus
    created_at: str
    updated_at: str


@dataclass(frozen=True)
class StarterState:
    starter_id: str
    capsule_id: str
    slot_type: str
    is_active: bool
    history: List[str] = field(default_factory=list)
    current_connection_id: Optional[str] = None


@dataclass(frozen=True)
class CapsuleState:
    capsule_id: str
    capsule_type: CapsuleType
    slots: Dict[str, Optional[StarterState]]
    connections: List[Connection] = field(default_factory=list)
    ledger_sequence: int = 0


class State:
    def __init__(self, capsule_id: str, capsule_type: CapsuleType):
        self.capsule_id = capsule_id
        self.capsule_type = capsule_type
        self._slots: Dict[str, Optional[StarterState]] = {}
        self._connections: List[Connection] = []
        self._sequence = 0
        
        # Initialize slots
        slot_types = ["friendship", "collaboration", "trust", "exchange", "alliance"]
        for slot_type in slot_types:
            self._slots[slot_type] = None

    def apply_event(self, event: Event) -> "State":
        new_state = State(self.capsule_id, self.capsule_type)
        new_state._slots = self._slots.copy()
        new_state._connections = self._connections.copy()
        new_state._sequence = self._sequence + 1
        return new_state

    def get_slot(self, slot_type: str) -> Optional[StarterState]:
        return self._slots.get(slot_type)

    def is_slot_empty(self, slot_type: str) -> bool:
        return self._slots.get(slot_type) is None

    def get_active_starters(self) -> List[StarterState]:
        return [starter for starter in self._slots.values() if starter and starter.is_active]

    def get_connections(self, status: Optional[ConnectionStatus] = None) -> List[Connection]:
        if not status:
            return self._connections.copy()
        return [conn for conn in self._connections if conn.status == status]

    def to_dict(self) -> dict:
        return {
            "capsule_id": self.capsule_id,
            "capsule_type": self.capsule_type.value,
            "slots": {
                slot_type: (starter.__dict__ if starter else None)
                for slot_type, starter in self._slots.items()
            },
            "connections": [conn.__dict__ for conn in self._connections],
            "sequence": self._sequence,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "State":
        capsule_type = CapsuleType(data["capsule_type"])
        state = cls(data["capsule_id"], capsule_type)
        state._sequence = data["sequence"]
        
        for slot_type, starter_data in data["slots"].items():
            if starter_data:
                starter = StarterState(**starter_data)
                state._slots[slot_type] = starter
            else:
                state._slots[slot_type] = None
        
        state._connections = [Connection(**conn_data) for conn_data in data["connections"]]
        return state
