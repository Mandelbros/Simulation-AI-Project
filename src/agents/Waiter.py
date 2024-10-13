from typing import List
from src.agents.Agent import Agent
from src.utils.utils import Position
from src.Order import Order
from src.Dish import Dish
from src.tasks.tasks import Task
from src.agents.rules import waiter_rules

class Waiter(Agent):
    def __init__(self, id, position: Position, rules_priority):
        super().__init__(id, position, "Waiter")
        self.tasks: List[Task] = []
        self.orders_queue: List[Order] = []
        self.dishes: List[Order] = []
        self.capacity = 2 # config
        self.at_kitchen = True
        self.dishes_at_kitchen = []
        self.cur_task = None
        self.rules_priority = rules_priority #lista con los indices de las reglas en orden de prioridad
    
    def add_task(self, task: Task, time, verbose):
        self.tasks.append(task)
        if verbose:
            print(f'\tWaiter {self.id} received new {task}, at time {time}.')

    def decide_action(self, time, verbose):
        for rule_index in self.rules_priority:
            waiter_rules[rule_index].evaluate(self, time, verbose)
    
    def work_on_task(self, i):
        self.cur_task = self.tasks.pop(i)

    def finish_cur_task(self, time, verbose):
        task = self.cur_task
        self.cur_task = None
        if verbose:
            print(f'\tWaiter {self.id} finished {task}, at time {time}.')

    def add_order(self, order: Order, time, verbose):
        self.orders_queue.append(order)
        if verbose:
            print(f'\tWaiter {self.id} received new {order}, at time {time}.')

    def add_dish(self, order: Order, time, verbose):
        self.dishes.append(order)
        if verbose:
            print(f'\tWaiter {self.id} took prepared {order}, at time {time}.')

    def is_free(self):
        return self.cur_task is None and len(self.tasks) == 0

    def has_capacity(self):
        return self.capacity > len(self.dishes)
    
    def __str__(self):
        return f"Waiter {self.id}"
    
    def __repr__(self):
        return f"Waiter {self.id}"