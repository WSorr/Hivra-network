from typing import Optional, List
from src.events.base import Event, InviteEvent, UserActionEvent, UserActionType, StarterEvent
from src.core.capsule import Capsule
from src.core.starter import Starter

class InvitationModule:
    def __init__(self, capsule: Capsule):
        self.capsule = capsule
    
    def handle_event(self, event: Event) -> Optional[List[Event]]:
        if isinstance(event, InviteEvent):
            return self._handle_invite(event)
        elif isinstance(event, UserActionEvent):
            return self._handle_user_action(event)
        return None
    
    def _handle_invite(self, event: InviteEvent) -> List[Event]:
        if event.target_capsule_id != self.capsule.id:
            return []
        
        relationship = self.capsule.get_relationship(event.sender_capsule_id)
        relationship.invited = True
        return []
    
    def _handle_user_action(self, event: UserActionEvent) -> List[Event]:
        if event.action_type == UserActionType.ACCEPT_INVITE:
            return self._handle_accept(event)
        elif event.action_type == UserActionType.REJECT_INVITE:
            return self._handle_reject(event)
        return []
    
    def _handle_accept(self, event: UserActionEvent) -> List[Event]:
        if not event.invite_sender_id:
            return []
        
        relationship = self.capsule.get_relationship(event.invite_sender_id)
        if not relationship.invited:
            return []
        
        relationship.invited = False
        
        if self.capsule.has_empty_slot():
            # TODO: Translate to English
            new_starter = Starter.generate(self.capsule.id)
            slot_idx = self.capsule.find_empty_slot()
            
            if slot_idx is not None:
                self.capsule.occupy_slot(slot_idx, new_starter.id)
                
                # TODO: Translate to English
                return [StarterEvent(
                    starter_id=new_starter.id,
                    source=self.capsule.id,
                    metadata={
                        "action": "starter_generated",
                        "from_invitation": True,
                        "invite_sender_id": event.invite_sender_id,
                        "original_starter": event.invite_starter_id
                    }
                )]
        
        return []
    
    def _handle_reject(self, event: UserActionEvent) -> List[Event]:
        if not event.invite_sender_id:
            return []
        
        relationship = self.capsule.get_relationship(event.invite_sender_id)
        if relationship.invited:
            relationship.invited = False
            
            if self.capsule.has_empty_slot():
                # TODO: Translate to English
                return [StarterEvent(
                    starter_id=event.invite_starter_id or "",
                    source=self.capsule.id,
                    metadata={
                        "action": "starter_burned",
                        "burned_from": event.invite_sender_id
                    }
                )]
        return []
