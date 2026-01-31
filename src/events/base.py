"""
Simple Event system for Hivra V1.
"""
from dataclasses import dataclass, field
from typing import Dict, Any
from datetime import datetime
from uuid import uuid4


@dataclass
class Event:
    """Simple event with all default fields."""
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
    def from_dict(cls, data: Dict[str, Any]) -> "Event":
        timestamp = data.get("timestamp")
        if timestamp:
            timestamp = datetime.fromisoformat(timestamp)
        else:
            timestamp = None
        
        event_id = data.get("event_id")
        if not event_id:
            event_id = str(uuid4())
        
        return cls(
            event_type=data.get("event_type", "event"),
            event_id=event_id,
            timestamp=timestamp or datetime.utcnow(),
            metadata=data.get("metadata", {})
        )
