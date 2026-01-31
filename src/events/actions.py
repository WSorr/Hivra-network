"""
Action events - burning, returning, generating starters.
"""
from dataclasses import dataclass, field
from typing import Optional, Dict, Any

from src.events.base import Event


@dataclass
class BurnEvent(Event):
    """Event for burning a starter."""
    starter_id: str
    capsule_id: str
    reason: str
    event_type: str = "burn"
    event_id: Optional[str] = None
    timestamp: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        super().__post_init__()


@dataclass
class ReturnEvent(Event):
    """Event for returning a starter."""
    starter_id: str
    from_capsule_id: str
    to_capsule_id: str
    connection_id: str
    event_type: str = "return"
    event_id: Optional[str] = None
    timestamp: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        super().__post_init__()


@dataclass
class GenerateEvent(Event):
    """Event for generating a new starter."""
    capsule_id: str
    slot_type: str
    based_on_starter_id: Optional[str] = None  # For inheritance from sender
    event_type: str = "generate"
    event_id: Optional[str] = None
    timestamp: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        super().__post_init__()
