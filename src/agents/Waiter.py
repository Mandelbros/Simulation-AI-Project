from typing import List
from src.agents.Agent import Agent
from src.agents.Customer import Customer
from src.utils.utils import Position

class Waiter(Agent):
    def __init__(self, id, position: Position):
        super().__init__(id, position)
        self.dests_queue: List[Customer] = []
    
    def add_dest(self, id):
        self.dests_queue.append(id)