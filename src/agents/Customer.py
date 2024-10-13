from src.agents.Agent import Agent
from src.utils.utils import Position

class Customer(Agent):
    def __init__(self, id, position: Position):
        super().__init__(id, position, "Customer")
        self.total_wating_time = 0
        self.cur_waiting_start_time = None
        self.table_id = None
        self.dish_served_temperature = None

    def start_waiting(self, time, verbose):
        self.stop_waiting(time, verbose)
        self.cur_waiting_start_time = time
        if verbose:
            print(f'\tCustomer {self.id} started waiting at time {time}.')

    def stop_waiting(self, time, verbose):
        if self.cur_waiting_start_time is not None:
            self.total_wating_time += time - self.cur_waiting_start_time
            if verbose:
                print(f'\tCustomer {self.id} stoped waiting at time {time} (waited for {time - self.cur_waiting_start_time}s).')
            self.cur_waiting_start_time = None

    def leave_tip(self, tip_percent, tip, time, verbose):
        if verbose:
            print(f'\tCustomer {self.id} waited a total of {self.total_wating_time}s, left {tip_percent}% of tip (${tip}), at time {time}.')

    def get_served(self, order, time, temperature, verbose):
        self.dish_served_temperature = temperature

    def __str__(self):
        return f"Customer {self.id}"
    
    def __repr__(self):
        return f"Customer {self.id}"