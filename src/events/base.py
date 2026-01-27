from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import uuid
from typing import Optional

class UserActionType(Enum):
    ACCEPT_INVITE = "accept_invite"
    REJECT_INVITE = "reject_invite"
    TOGGLE_STATE = "toggle_state"

@dataclass
class Event:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    source: str = ""

@dataclass
class StarterEvent(Event):
    starter_id: str = ""
    metadata: dict = field(default_factory=dict)

@dataclass  
class InviteEvent(Event):
    sender_capsule_id: str = ""
    target_capsule_id: str = ""
    sender_starter_id: str = ""

@dataclass
class UserActionEvent(Event):
    action_type: UserActionType = UserActionType.TOGGLE_STATE
    target_capsule_id: str = ""
    invite_sender_id: Optional[str] = None
    invite_starter_id: Optional[str] = None
    state_name: Optional[str] = None
