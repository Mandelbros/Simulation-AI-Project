from typing import List
from src.utils.utils import Place, Position
from src.Order import Order

class Kitchen(Place):
    def __init__(self, id, position: Position, cooking_capacity):
        super().__init__(id, position)
        self.orders_queue: List[Order] = []
        self.prepared_orders: List[Order] = []
        self.cooking_capacity = cooking_capacity
        self.in_progress = 0
    
    def add_order(self, order: Order, time, verbose):
        self.orders_queue.append(order)
        if verbose:
            print(f'\tThe kitchen received a new {order}, at time {time}.')
    
    def has_capacity(self):
        return self.in_progress < self.cooking_capacity
    
    def start_next_order(self, time, verbose):
        self.in_progress += 1
        order = self.orders_queue.pop(0)
        if verbose:
            print(f'\tThe kitchen started cooking {order}, at time {time}.')
               
    def finish_order(self, order: Order, time, verbose):
        self.in_progress -= 1
        if verbose:
            print(f'\tThe kitchen finished cooking {order}, at time {time}.')