"""
Simple event definitions without complex inheritance.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from datetime import datetime

from src.events.base_fixed import BaseEvent


@dataclass
class LinkIntentEvent(BaseEvent):
    """Link intent event."""
    sender_id: str
    recipient_id: str
    starter_id: str
    starter_type: str
    invitation_data: Dict[str, Any] = field(default_factory=dict)
    event_type: str = "link_intent"
    event_id: Optional[str] = None
    timestamp: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AcceptIntentEvent(LinkIntentEvent):
    """Accept intent event."""
    event_type: str = "accept_intent"


@dataclass
class RejectIntentEvent(LinkIntentEvent):
    """Reject intent event."""
    reason: Optional[str] = None
    event_type: str = "reject_intent"


@dataclass
class ConfirmAcceptEvent(BaseEvent):
    """Confirm accept event."""
    connection_id: str
    starter_id: str
    new_starter_id: Optional[str] = None
    event_type: str = "confirm_accept"
    event_id: Optional[str] = None
    timestamp: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ConfirmRejectEvent(BaseEvent):
    """Confirm reject event."""
    connection_id: str
    starter_id: str
    burned: bool = False
    event_type: str = "confirm_reject"
    event_id: Optional[str] = None
    timestamp: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BurnEvent(BaseEvent):
    """Burn event."""
    starter_id: str
    capsule_id: str
    reason: str
    event_type: str = "burn"
    event_id: Optional[str] = None
    timestamp: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ReturnEvent(BaseEvent):
    """Return event."""
    starter_id: str
    from_capsule_id: str
    to_capsule_id: str
    connection_id: str
    event_type: str = "return"
    event_id: Optional[str] = None
    timestamp: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GenerateEvent(BaseEvent):
    """Generate event."""
    capsule_id: str
    slot_type: str
    based_on_starter_id: Optional[str] = None
    event_type: str = "generate"
    event_id: Optional[str] = None
    timestamp: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class InvitationAcceptedEvent(BaseEvent):
    """Invitation accepted event."""
    invitation_id: str
    acceptor_id: str
    new_starter_id: Optional[str] = None
    event_type: str = "invitation_accepted"
    event_id: Optional[str] = None
    timestamp: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class InvitationRejectedEvent(BaseEvent):
    """Invitation rejected event."""
    invitation_id: str
    rejector_id: str
    reason: Optional[str] = None
    burned: bool = False
    event_type: str = "invitation_rejected"
    event_id: Optional[str] = None
    timestamp: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


# Register all events
BaseEvent.register_event(LinkIntentEvent)
BaseEvent.register_event(AcceptIntentEvent)
BaseEvent.register_event(RejectIntentEvent)
BaseEvent.register_event(ConfirmAcceptEvent)
BaseEvent.register_event(ConfirmRejectEvent)
BaseEvent.register_event(BurnEvent)
BaseEvent.register_event(ReturnEvent)
BaseEvent.register_event(GenerateEvent)
BaseEvent.register_event(InvitationAcceptedEvent)
BaseEvent.register_event(InvitationRejectedEvent)
