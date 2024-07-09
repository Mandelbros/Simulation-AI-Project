class Event:
    def __init__(self, time):
        self.time = time

    def __lt__(self, other:'Event'):
        return self.time < other.time
