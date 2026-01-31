"""
Event Bus - simple version.
"""
from typing import Dict, List, Callable, Any, Optional
from dataclasses import dataclass

from src.events import Event
from src.core.ledger import Ledger
from src.core.state import State


@dataclass
class EventHandler:
    handler: Callable[[Event, Ledger, State], Optional[Event]]
    priority: int = 0


class EventBus:
    def __init__(self):
        self._handlers: Dict[str, List[EventHandler]] = {}
    
    def subscribe(self, event_type: str, handler: Callable, priority: int = 0) -> None:
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(EventHandler(handler, priority))
        self._handlers[event_type].sort(key=lambda h: h.priority, reverse=True)
    
    def unsubscribe(self, event_type: str, handler: Callable) -> None:
        if event_type in self._handlers:
            self._handlers[event_type] = [
                h for h in self._handlers[event_type] if h.handler != handler
            ]
    
    def publish(self, event: Event, ledger: Ledger, state: State) -> List[Event]:
        event_type = event.event_type
        generated_events: List[Event] = []
        
        if event_type in self._handlers:
            for handler_info in self._handlers[event_type]:
                try:
                    result = handler_info.handler(event, ledger, state)
                    if result:
                        generated_events.append(result)
                except Exception as e:
                    print(f"Error in handler for {event_type}: {e}")
        
        return generated_events
    
    def process_event_chain(self, initial_event: Event, ledger: Ledger, state: State) -> State:
        events_to_process = [initial_event]
        current_state = state
        
        while events_to_process:
            event = events_to_process.pop(0)
            generated = self.publish(event, ledger, current_state)
            new_state = current_state.apply_event(event)
            current_state = new_state
            events_to_process.extend(generated)
        
        return current_state
