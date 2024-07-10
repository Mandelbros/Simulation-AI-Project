from src.agents.Agent import Agent
from utils.utils import Position

class Customer(Agent):
    def __init__(self, id, position: Position):
        super.__init__(id, position)
        self.total_wating_time = 0
        self.cur_waiting_start_time = None

    def start_waiting(self, cur_time):
        self.stop_waiting(cur_time)
        self.cur_waiting_start_time = cur_time

    def stop_waiting(self, cur_time):
        if self.cur_waiting_start_time is not None:
            self.total_wating_time = cur_time - self.cur_waiting_start_time
            self.cur_waiting_start_time = None