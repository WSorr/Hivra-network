"""
Event system for Hivra CapsuleNet V1.
"""
from src.events.base import Event
from src.events.factories import create_invitation_event

__all__ = ['Event', 'create_invitation_event']
