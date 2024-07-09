class Event:
    def __init__(self, time, event_type):
        self.time = time
        self.event_type = event_type 

    def __lt__(self, other:'Event'):
        return self.time < other.time
