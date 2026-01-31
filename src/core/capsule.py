"""
Capsule, Starter, and Slot classes with binary starter nature.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Set, Any
from uuid import uuid4


class CapsuleType(Enum):
    """Type of capsule."""
    GENESIS = "genesis"
    PROTO = "proto"
    LINKED = "linked"


class StarterStatus(Enum):
    """Binary status of a starter."""
    OFF = "off"
    ON = "on"


@dataclass
class Slot:
    """Slot for holding a starter."""
    slot_type: str
    starter_id: Optional[str] = None
    is_locked: bool = False


@dataclass
class Starter:
    """
    Binary starter - abstract switch controlled by events.
    """
    starter_id: str
    capsule_id: str
    slot_type: str
    status: StarterStatus = StarterStatus.OFF
    created_at: str = field(default_factory=lambda: str(uuid4()))
    history: List[str] = field(default_factory=list)  # List of event IDs
    traits: Dict[str, Any] = field(default_factory=dict)
    current_connection_id: Optional[str] = None
    
    def toggle(self) -> None:
        """Toggle status - only called by event mechanics."""
        self.status = StarterStatus.ON if self.status == StarterStatus.OFF else StarterStatus.OFF
    
    def add_event(self, event_id: str) -> None:
        """Add event to history."""
        self.history.append(event_id)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to serializable dict."""
        return {
            "starter_id": self.starter_id,
            "capsule_id": self.capsule_id,
            "slot_type": self.slot_type,
            "status": self.status.value,
            "created_at": self.created_at,
            "history": self.history.copy(),
            "traits": self.traits.copy(),
            "current_connection_id": self.current_connection_id,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Starter":
        """Create from dict."""
        starter = cls(
            starter_id=data["starter_id"],
            capsule_id=data["capsule_id"],
            slot_type=data["slot_type"],
            status=StarterStatus(data["status"]),
            created_at=data["created_at"],
            history=data["history"].copy(),
            traits=data["traits"].copy(),
            current_connection_id=data.get("current_connection_id"),
        )
        return starter


@dataclass
class Capsule:
    """Capsule entity."""
    capsule_id: str
    capsule_type: CapsuleType
    slots: Dict[str, Slot] = field(default_factory=dict)
    connections: Set[str] = field(default_factory=set)  # Set of connection IDs
    ledger_id: Optional[str] = None
    
    def __post_init__(self):
        """Initialize capsule based on type."""
        # Define starter types with emojis
        slot_types = {
            "⚡ Juice": "juice",
            "💥 Spark": "spark", 
            "🌱 Seed": "seed",
            "📡 Pulse": "pulse",
            "🔥 Kick": "kick"
        }
        
        # Initialize empty slots with display names
        for display_name, internal_name in slot_types.items():
            self.slots[display_name] = Slot(slot_type=display_name)
        
        # If genesis, generate starters for all slots
        if self.capsule_type == CapsuleType.GENESIS:
            for display_name in slot_types.keys():
                starter = Starter(
                    starter_id=str(uuid4()),
                    capsule_id=self.capsule_id,
                    slot_type=display_name,
                    status=StarterStatus.OFF,
                )
                self.slots[display_name].starter_id = starter.starter_id
    
    def get_slot(self, slot_display_name: str) -> Optional[Slot]:
        """Get slot by display name."""
        return self.slots.get(slot_display_name)
    
    def is_slot_empty(self, slot_display_name: str) -> bool:
        """Check if slot is empty."""
        slot = self.get_slot(slot_display_name)
        return slot is None or slot.starter_id is None
    
    def get_starter_id(self, slot_display_name: str) -> Optional[str]:
        """Get starter ID in slot, if any."""
        slot = self.get_slot(slot_display_name)
        return slot.starter_id if slot else None
    
    def add_connection(self, connection_id: str) -> None:
        """Add connection to capsule."""
        self.connections.add(connection_id)
    
    def remove_connection(self, connection_id: str) -> None:
        """Remove connection from capsule."""
        self.connections.discard(connection_id)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert capsule to dict."""
        return {
            "capsule_id": self.capsule_id,
            "capsule_type": self.capsule_type.value,
            "slots": {
                slot_type: {
                    "slot_type": slot.slot_type,
                    "starter_id": slot.starter_id,
                    "is_locked": slot.is_locked,
                }
                for slot_type, slot in self.slots.items()
            },
            "connections": list(self.connections),
            "ledger_id": self.ledger_id,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Capsule":
        """Create capsule from dict."""
        capsule = cls(
            capsule_id=data["capsule_id"],
            capsule_type=CapsuleType(data["capsule_type"]),
        )
        
        # Restore slots
        for slot_type, slot_data in data["slots"].items():
            slot = Slot(
                slot_type=slot_data["slot_type"],
                starter_id=slot_data["starter_id"],
                is_locked=slot_data["is_locked"],
            )
            capsule.slots[slot_type] = slot
        
        # Restore connections
        capsule.connections = set(data["connections"])
        capsule.ledger_id = data.get("ledger_id")
        
        return capsule
