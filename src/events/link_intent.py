"""
Link intent events - initiating connections.
"""
from dataclasses import dataclass, field
from typing import Optional, Dict, Any

from src.events.base import Event


@dataclass
class LinkIntent(Event):
    """Base class for link intent events."""
    sender_id: str
    recipient_id: str
    starter_id: str
    starter_type: str
    invitation_data: Dict[str, Any] = field(default_factory=dict)
    event_type: str = "link_intent"
    event_id: Optional[str] = None
    timestamp: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        super().__post_init__()


@dataclass
class AcceptIntent(LinkIntent):
    """Intent to accept a connection."""
    event_type: str = "accept_intent"
    
    def __post_init__(self):
        super().__post_init__()


@dataclass
class RejectIntent(LinkIntent):
    """Intent to reject a connection."""
    reason: Optional[str] = None
    event_type: str = "reject_intent"
    
    def __post_init__(self):
        super().__post_init__()
