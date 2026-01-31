"""
Simple event system without inheritance issues.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from datetime import datetime
from uuid import uuid4


@dataclass
class SimpleEvent:
    """Simple event - all fields have defaults."""
    event_type: str = "event"
    event_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_type": self.event_type,
            "event_id": self.event_id,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SimpleEvent":
        timestamp = data.get("timestamp")
        if timestamp:
            timestamp = datetime.fromisoformat(timestamp)
        
        return cls(
            event_type=data.get("event_type", "event"),
            event_id=data.get("event_id", str(uuid4())),
            timestamp=timestamp or datetime.utcnow(),
            metadata=data.get("metadata", {})
        )


# Factory functions
def create_invitation(invitation_id: str, sender_id: str, recipient_id: str, 
                     starter_id: str, capsule_id: str, slot_type: str) -> SimpleEvent:
    event = SimpleEvent(event_type="invitation")
    event.metadata.update({
        "invitation_id": invitation_id,
        "sender_id": sender_id,
        "recipient_id": recipient_id,
        "starter_id": starter_id,
        "capsule_id": capsule_id,
        "slot_type": slot_type
    })
    return event
