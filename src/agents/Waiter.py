from src.agents.Agent import Agent
from src.utils.utils import Position

class Waiter(Agent):
    def __init__(self, id, position: Position):
        super().__init__(id, position)