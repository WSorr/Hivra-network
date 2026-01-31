"""
Fixed base event classes without complex inheritance issues.
"""
from dataclasses import dataclass, field, asdict
from typing import Dict, Any, Optional, ClassVar
from datetime import datetime
import json
from uuid import uuid4


@dataclass
class BaseEvent:
    """Base event class with proper argument ordering."""
    # Required arguments first
    event_type: str
    
    # Optional arguments with defaults
    event_id: Optional[str] = None
    timestamp: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Class variable to track event class mapping
    _event_registry: ClassVar[Dict[str, type]] = {}
    
    def __post_init__(self):
        if self.event_id is None:
            self.event_id = str(uuid4())
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to serializable dict."""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat() if self.timestamp else None
        # Store the class name for deserialization
        data['_class'] = self.__class__.__name__
        return data
    
    @classmethod
    def register_event(cls, event_class: type):
        """Register an event class for deserialization."""
        cls._event_registry[event_class.__name__] = event_class
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BaseEvent":
        """Create event from dict."""
        # Handle timestamp conversion
        if 'timestamp' in data and data['timestamp']:
            data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        else:
            data['timestamp'] = None
        
        # Remove the class marker
        class_name = data.pop('_class', None)
        
        if class_name and class_name in cls._event_registry:
            event_class = cls._event_registry[class_name]
            return event_class(**data)
        
        # Fall back to BaseEvent
        return cls(**data)
    
    def to_json(self) -> str:
        """Serialize event to JSON."""
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_json(cls, json_str: str) -> "BaseEvent":
        """Create event from JSON."""
        return cls.from_dict(json.loads(json_str))


# Register BaseEvent itself
BaseEvent.register_event(BaseEvent)


@dataclass
class StarterEvent(BaseEvent):
    """Event related to starter operations."""
    # Required arguments first
    starter_id: str
    capsule_id: str
    event_type: str = field(default="starter")
    
    # Optional arguments with defaults (inherit from parent)
    event_id: Optional[str] = None
    timestamp: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


# Register StarterEvent
BaseEvent.register_event(StarterEvent)


@dataclass
class InvitationEvent(StarterEvent):
    """Invitation event."""
    # Required arguments first
    invitation_id: str
    sender_id: str
    recipient_id: str
    slot_type: str
    
    # Inherit other fields with proper defaults
    event_type: str = field(default="invitation")
    event_id: Optional[str] = None
    timestamp: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


# Register InvitationEvent
BaseEvent.register_event(InvitationEvent)


# Simple Event alias for compatibility
Event = BaseEvent
