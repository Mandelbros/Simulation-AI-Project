from typing import List
from src.agents.Rule import Rule
from src.tasks.tasks import *

class TakeFirstDish(Rule):
    def __init__(self):
        self.weight = 1
        self.description = 'If the waiter has capacity left and no current task and he is at the kitchen and it has at least a prepared dish, they take the first prepared dish'

    def evaluate(self, waiter, time, verbose):
        if waiter.cur_task is None and waiter.at_kitchen and len(waiter.dishes_at_kitchen) > 0 and waiter.has_capacity():
            order = waiter.dishes_at_kitchen[0]
            waiter.cur_task = TakeDish(order)


class DeliverFirstDish(Rule):
    def __init__(self):
        self.weight = 2 # before this update it didn't exist
        self.description = 'If the waiter has at least a dish and no current task, they deliver the first taken dish'

    def evaluate(self, waiter, time, verbose):
        if waiter.cur_task is None and len(waiter.dishes) > 0:
            order = waiter.dishes.pop(0)
            waiter.cur_task = DeliverDish(order)


class CollectFirstBill(Rule):
    def __init__(self):
        self.weight = 3 # before this update it didn't exist
        self.description = 'If the waiter has at least a bill to collect and no current task, they collect the bill from their first task of this type'

    def evaluate(self, waiter, time, verbose):
        if waiter.cur_task is not None:
            return
        for i in range(len(waiter.tasks)):
            if isinstance(waiter.tasks[i], CollectBill):
                waiter.work_on_task(i)
                return
            

class TakeFirstOrder(Rule):
    def __init__(self):
        self.weight = 4 # before this update it didn't exist
        self.description = 'If the waiter has at least an order to take no current task, they take the order from their first task of this type'

    def evaluate(self, waiter, time, verbose):
        if waiter.cur_task is not None:
            return
        for i in range(len(waiter.tasks)):
            if isinstance(waiter.tasks[i], TakeOrder):
                waiter.work_on_task(i)
                return
            

class GoToKitchen(Rule):
    def __init__(self):
        self.weight = 5 # before this update it had weight 3
        self.description = 'If the waiter has no current task and they are not in the kitchen, they go there'

    def evaluate(self, waiter, time, verbose):
        if waiter.cur_task is None and not waiter.at_kitchen:
            waiter.cur_task = ReturnToKitchen()


class DoFirstTask(Rule):
    def __init__(self):
        self.weight = 6 # before this update it had weight 2
        self.description = 'If the waiter has no current task and they have at least a task remaining, they do the first remaining task'

    def evaluate(self, waiter, time, verbose):
        if waiter.cur_task is None and len(waiter.tasks) > 0:
            waiter.work_on_task(0)
  
waiter_rules : List[Rule] = [TakeFirstDish(), DeliverFirstDish(), CollectFirstBill(), TakeFirstOrder(), GoToKitchen(), DoFirstTask()]
waiter_rules.sort(key = lambda x: x.weight)