"""
Factory functions for creating specific events.
"""
from src.events.base import Event


def create_invitation_event(
    invitation_id: str,
    sender_id: str,
    recipient_id: str,
    starter_id: str,
    capsule_id: str,
    slot_type: str
) -> Event:
    """Create an invitation event."""
    event = Event(event_type="invitation")
    event.metadata.update({
        "invitation_id": invitation_id,
        "sender_id": sender_id,
        "recipient_id": recipient_id,
        "starter_id": starter_id,
        "capsule_id": capsule_id,
        "slot_type": slot_type
    })
    return event
