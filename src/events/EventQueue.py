import heapq
from typing import List
from events.Event import Event

class EventQueue:
    def __init__(self):
        self.events:List[Event] = []

    def add_event(self, event:Event):
        heapq.heappush(self.events, event)

    def next_event(self):
        return heapq.heappop(self.events) if self.events else None