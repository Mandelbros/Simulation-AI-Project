from src.events.Event import Event
from src.agents.Customer import Customer

class CustomerArrival(Event):
    def __init__(self, time, customer:Customer):
        super().__init__(time)
        self.customer = customer    