from src.agents.Customer import Customer

class Event:
    def __init__(self, time):
        self.time = time

    def __lt__(self, other:'Event'):
        return self.time < other.time
    
class CustomerArrival(Event):
    def __init__(self, time, customer:Customer):
        super().__init__(time)
        self.customer = customer    