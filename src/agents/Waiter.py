from typing import List
from src.agents.Agent import Agent
from src.agents.Customer import Customer
from src.utils.utils import Position
from src.Order import Order
from src.Dish import Dish

class Waiter(Agent):
    def __init__(self, id, position: Position):
        super().__init__(id, position, "Waiter")
        self.dests_queue: List[Customer] = []
        self.orders_queue: List[Order] = []
        self.dishes: List[Dish] = []
    
    def add_dest(self, id, time, verbose):
        self.dests_queue.append(id)
        if verbose:
            print(f'\tWaiter {self.id} received new destination to Place {id}, at time {time}.')

    def add_order(self, order: Order, time, verbose):
        self.orders_queue.append(order)
        if verbose:
            print(f'\tWaiter {self.id} received new {order}, at time {time}.')

    def is_free(self):
        return len(self.dests_queue) == 0
    
    def __str__(self):
        return f"Waiter {self.id}"
    
    def __repr__(self):
        return f"Waiter {self.id}"