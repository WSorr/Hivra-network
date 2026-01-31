"""
Ledger - append-only log of events.
"""
import json
from datetime import datetime
from typing import List, Any, Dict, Optional

from src.events import Event


class LedgerEntry:
    def __init__(
        self,
        event: Event,
        timestamp: Optional[datetime] = None,
        capsule_id: Optional[str] = None,
        sequence_number: int = 0,
        tags: Optional[List[str]] = None,
    ):
        self.id = event.event_id
        self.event = event
        self.timestamp = timestamp or datetime.utcnow()
        self.capsule_id = capsule_id
        self.sequence_number = sequence_number
        self.tags = tags or []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "event": self.event.to_dict(),
            "timestamp": self.timestamp.isoformat(),
            "capsule_id": self.capsule_id,
            "sequence_number": self.sequence_number,
            "tags": self.tags,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LedgerEntry":
        event = Event.from_dict(data["event"])
        return cls(
            event=event,
            timestamp=datetime.fromisoformat(data["timestamp"]),
            capsule_id=data["capsule_id"],
            sequence_number=data["sequence_number"],
            tags=data["tags"],
        )


class Ledger:
    def __init__(self, capsule_id: str):
        self.capsule_id = capsule_id
        self.entries: List[LedgerEntry] = []
        self._sequence_counter = 0

    def append(self, event: Event, tags: Optional[List[str]] = None) -> LedgerEntry:
        self._sequence_counter += 1
        entry = LedgerEntry(
            event=event,
            capsule_id=self.capsule_id,
            sequence_number=self._sequence_counter,
            tags=tags or [],
        )
        self.entries.append(entry)
        return entry

    def get_entries(self, tags: Optional[List[str]] = None) -> List[LedgerEntry]:
        if not tags:
            return self.entries.copy()
        return [entry for entry in self.entries if any(tag in entry.tags for tag in tags)]

    def get_last_entry(self) -> Optional[LedgerEntry]:
        return self.entries[-1] if self.entries else None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "capsule_id": self.capsule_id,
            "entries": [entry.to_dict() for entry in self.entries],
            "sequence_counter": self._sequence_counter,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Ledger":
        ledger = cls(capsule_id=data["capsule_id"])
        ledger._sequence_counter = data["sequence_counter"]
        ledger.entries = [LedgerEntry.from_dict(entry) for entry in data["entries"]]
        return ledger

    def save_to_file(self, path: str):
        with open(path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load_from_file(cls, path: str) -> "Ledger":
        with open(path, 'r') as f:
            data = json.load(f)
        return cls.from_dict(data)
