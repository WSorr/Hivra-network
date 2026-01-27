from typing import List, Dict, Type
from src.events.base import Event

class EventBus:
    def __init__(self):
        self._handlers: Dict[Type[Event], List] = {}
    
    def subscribe(self, event_type: Type[Event], handler):
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)
    
    def publish(self, event: Event) -> List[Event]:
        output_events = []
        
        event_type = type(event)
        if event_type in self._handlers:
            for handler in self._handlers[event_type]:
                result = handler(event)
                if result:
                    if isinstance(result, list):
                        output_events.extend(result)
                    elif isinstance(result, Event):
                        output_events.append(result)
        
        return output_events
