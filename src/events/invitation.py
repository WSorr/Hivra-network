"""
Invitation events - handling invitations between capsules.
"""
from dataclasses import dataclass, field
from typing import Optional, Dict, Any

from src.events.base import Event


@dataclass
class InvitationAcceptedEvent(Event):
    """Event when invitation is accepted."""
    invitation_id: str
    acceptor_id: str
    new_starter_id: Optional[str] = None  # For proto capsules
    event_type: str = "invitation_accepted"
    event_id: Optional[str] = None
    timestamp: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        super().__post_init__()


@dataclass
class InvitationRejectedEvent(Event):
    """Event when invitation is rejected."""
    invitation_id: str
    rejector_id: str
    reason: Optional[str] = None
    burned: bool = False  # Whether starter was burned
    event_type: str = "invitation_rejected"
    event_id: Optional[str] = None
    timestamp: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        super().__post_init__()
