from typing import List
from src.agents.Agent import Agent
from src.utils.utils import Position
from src.Order import Order
from src.Dish import Dish
from src.requests.requests import Request

class Waiter(Agent):
    def __init__(self, id, position: Position):
        super().__init__(id, position, "Waiter")
        self.requests_queue: List[Request] = []
        self.orders_queue: List[Order] = []
        self.dishes: List[Dish] = []
    
    def add_request(self, request: Request, time, verbose):
        self.requests_queue.append(request)
        if verbose:
            print(f'\tWaiter {self.id} received new {request}, at time {time}.')

    def next_request(self):
        return self.requests_queue[0]

    def finish_next_request(self, time, verbose):
        request = self.requests_queue.pop(0)
        if verbose:
            print(f'\tWaiter {self.id} finished {request}, at time {time}.')

    def add_order(self, order: Order, time, verbose):
        self.orders_queue.append(order)
        if verbose:
            print(f'\tWaiter {self.id} received new {order}, at time {time}.')

    def is_free(self):
        return len(self.requests_queue) == 0
    
    def __str__(self):
        return f"Waiter {self.id}"
    
    def __repr__(self):
        return f"Waiter {self.id}"