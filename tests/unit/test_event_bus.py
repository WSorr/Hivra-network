import pytest
from src.coordinator.event_bus import EventBus
from src.events.base import Event

def test_bus_subscription():
    bus = EventBus()
    def handler(event):
        return []
    
    bus.subscribe(Event, handler)
    assert Event in bus._handlers
    assert len(bus._handlers[Event]) == 1

def test_bus_publish():
    bus = EventBus()
    results = []
    
    def handler(event):
        results.append(event.source)
        return []
    
    bus.subscribe(Event, handler)
    event = Event(source="test")
    bus.publish(event)
    
    assert results == ["test"]
