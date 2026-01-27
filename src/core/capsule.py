from dataclasses import dataclass, field
from typing import Dict, Optional
from enum import Enum

class CapsuleType(Enum):
    """Capsule types (logical, not privileged)"""
    GENESIS = "genesis"
    PROTO = "proto"
    LINKED = "linked"

@dataclass
class RelationshipState:
    """Connection states between capsule pair (toggle flags)"""
    invited: bool = False
    trusted: bool = False
    linked: bool = False
    ignored: bool = False
    
    def toggle(self, state_name: str) -> None:
        """Toggle any state (ON/OFF logic)"""
        if hasattr(self, state_name):
            setattr(self, state_name, not getattr(self, state_name))

@dataclass
class Slot:
    """Slot for starter storage"""
    EMPTY = "empty"
    OCCUPIED = "occupied"
    
    state: str = EMPTY
    starter_id: Optional[str] = None

@dataclass
class Capsule:
    """Autonomous network participant"""
    id: str
    capsule_type: CapsuleType
    slots: Dict[int, Slot] = field(default_factory=lambda: {i: Slot() for i in range(5)})
    relationships: Dict[str, RelationshipState] = field(default_factory=dict)
    
    def get_relationship(self, other_id: str) -> RelationshipState:
        """Get or create relationship state with another capsule"""
        if other_id not in self.relationships:
            self.relationships[other_id] = RelationshipState()
        return self.relationships[other_id]
    
    def has_empty_slot(self) -> bool:
        """Check if capsule has empty slot for new starter"""
        return any(slot.state == Slot.EMPTY for slot in self.slots.values())
    
    def find_empty_slot(self) -> Optional[int]:
        """Find first empty slot index"""
        for idx, slot in self.slots.items():
            if slot.state == Slot.EMPTY:
                return idx
        return None
    
    def occupy_slot(self, slot_idx: int, starter_id: str) -> bool:
        """Occupy slot with starter, returns success"""
        if slot_idx in self.slots and self.slots[slot_idx].state == Slot.EMPTY:
            self.slots[slot_idx].state = Slot.OCCUPIED
            self.slots[slot_idx].starter_id = starter_id
            return True
        return False
    
    def free_slot(self, slot_idx: int) -> None:
        """Free slot (set to empty)"""
        if slot_idx in self.slots:
            self.slots[slot_idx].state = Slot.EMPTY
            self.slots[slot_idx].starter_id = None
