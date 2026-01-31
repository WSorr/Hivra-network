"""
Base event classes.
"""
from dataclasses import dataclass, asdict, field
from typing import Dict, Any, Optional
from datetime import datetime
import json
from uuid import uuid4


@dataclass
class Event:
    """Base event class."""
    event_type: str
    event_id: Optional[str] = None
    timestamp: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if self.event_id is None:
            self.event_id = str(uuid4())
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to serializable dict."""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat() if self.timestamp else None
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Event":
        """Create event from dict."""
        # Handle timestamp conversion
        if 'timestamp' in data and data['timestamp']:
            data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        else:
            data['timestamp'] = None
        
        # Create appropriate event subclass based on event_type
        event_type = data.get('event_type', '')
        
        # Import here to avoid circular imports
        if event_type in ['link_intent', 'accept_intent', 'reject_intent']:
            from src.events.link_intent import LinkIntent, AcceptIntent, RejectIntent
            if event_type == 'accept_intent':
                return AcceptIntent(**data)
            elif event_type == 'reject_intent':
                return RejectIntent(**data)
            else:
                return LinkIntent(**data)
        elif event_type in ['confirm_accept', 'confirm_reject']:
            from src.events.confirm import ConfirmAccept, ConfirmReject
            if event_type == 'confirm_accept':
                return ConfirmAccept(**data)
            else:
                return ConfirmReject(**data)
        elif event_type in ['burn', 'return', 'generate']:
            from src.events.actions import BurnEvent, ReturnEvent, GenerateEvent
            if event_type == 'burn':
                return BurnEvent(**data)
            elif event_type == 'return':
                return ReturnEvent(**data)
            else:
                return GenerateEvent(**data)
        elif event_type in ['invitation', 'invitation_accepted', 'invitation_rejected']:
            from src.events.invitation import InvitationEvent, InvitationAcceptedEvent, InvitationRejectedEvent
            if event_type == 'invitation':
                return InvitationEvent(**data)
            elif event_type == 'invitation_accepted':
                return InvitationAcceptedEvent(**data)
            else:
                return InvitationRejectedEvent(**data)
        elif event_type == 'starter':
            return StarterEvent(**data)
        else:
            # Return base Event for unknown types
            return cls(**data)
    
    def to_json(self) -> str:
        """Serialize event to JSON."""
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_json(cls, json_str: str) -> "Event":
        """Create event from JSON."""
        return cls.from_dict(json.loads(json_str))


@dataclass
class StarterEvent(Event):
    """Event related to starter operations."""
    starter_id: str
    capsule_id: str
    
    def __post_init__(self):
        super().__post_init__()
        if self.event_type == "starter":
            self.event_type = "starter"


@dataclass
class InvitationEvent(StarterEvent):
    """Invitation event."""
    invitation_id: str
    sender_id: str
    recipient_id: str
    slot_type: str
    
    def __post_init__(self):
        super().__post_init__()
        if self.event_type == "starter":
            self.event_type = "invitation"
