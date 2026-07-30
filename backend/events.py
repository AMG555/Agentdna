"""Minimal internal domain event bus for the modular monolith."""
from collections import defaultdict
class EventBus:
    def __init__(self): self.handlers=defaultdict(list); self.history=[]
    def subscribe(self,event,handler): self.handlers[event].append(handler)
    def publish(self,event,payload=None):
        record={'event':event,'payload':payload or {}}; self.history.append(record)
        for handler in self.handlers[event]: handler(record)
        return record
event_bus=EventBus()
