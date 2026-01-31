"""
Confirmation events - confirming intent outcomes.
"""
from dataclasses import dataclass, field
from typing import Optional, Dict, Any

from src.events.base import Event


@dataclass
class ConfirmAccept(Event):
    """Confirmation that accept was processed."""
    connection_id: str
    starter_id: str
    new_starter_id: Optional[str] = None  # For proto capsules generating starters
    event_type: str = "confirm_accept"
    event_id: Optional[str] = None
    timestamp: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        super().__post_init__()


@dataclass
class ConfirmReject(Event):
    """Confirmation that reject was processed."""
    connection_id: str
    starter_id: str
    burned: bool = False  # Whether starter was burned
    event_type: str = "confirm_reject"
    event_id: Optional[str] = None
    timestamp: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        super().__post_init__()
