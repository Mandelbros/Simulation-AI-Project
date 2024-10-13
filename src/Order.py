from src.Dish import Dish
from src.agents.Customer import Customer

class Order:
    def __init__(self, dish: Dish, customer: Customer):
        self.dish = dish
        self.customer = customer
        self.preparation_time = None
        self.initial_temperature = None

    def __str__(self):
        return f"Order of {self.dish} from {self.customer}"
    
    def __repr__(self):
        return f"Order of {self.dish} from {self.customer}"