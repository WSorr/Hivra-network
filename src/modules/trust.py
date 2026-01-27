from typing import Optional, List
from src.events.base import Event, UserActionEvent, UserActionType, StarterEvent
from src.core.capsule import Capsule

class TrustModule:
    def __init__(self, capsule: Capsule):
        self.capsule = capsule
    
    def handle_event(self, event: Event) -> Optional[List[Event]]:
        if isinstance(event, UserActionEvent):
            if (event.action_type == UserActionType.TOGGLE_STATE and 
                event.state_name == 'trusted'):
                return self._toggle_trust(event)
        
        elif isinstance(event, StarterEvent):
            if event.metadata.get('action') == 'starter_generated':
                return self._handle_starter_generated(event)
        
        return None
    
    def _toggle_trust(self, event: UserActionEvent) -> List[Event]:
        if event.target_capsule_id:
            relationship = self.capsule.get_relationship(event.target_capsule_id)
            relationship.toggle('trusted')
        return []
    
    def _handle_starter_generated(self, event: StarterEvent) -> List[Event]:
        # TODO: Translate to English
        if event.metadata.get('from_invitation'):
            sender_id = event.metadata.get('invite_sender_id')
            if sender_id:
                relationship = self.capsule.get_relationship(sender_id)
                relationship.trusted = True
        return []
