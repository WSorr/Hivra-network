"""
Event system - simple version.
"""
from src.events.base_simple import SimpleEvent, create_invitation

Event = SimpleEvent
create_invitation_event = create_invitation

__all__ = ['Event', 'create_invitation_event']
