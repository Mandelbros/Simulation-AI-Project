from src.agents.Customer import Customer
from src.Order import Order

class Task:
    pass
    
class TakeOrder(Task):
    def __init__(self, customer: Customer):
        self.customer = customer

    def __str__(self):
        return f"Task: take order of {self.customer}"
    
    def __repr__(self):
        return f"Task: take order of {self.customer}"
    
class TakeDish(Task):
    def __init__(self, order: Order):
        self.order = order

    def __str__(self):
        return f"Task: take {self.order.dish}"
    
    def __repr__(self):
        return f"Task: take {self.order.dish}"

class DeliverDish(Task):
    def __init__(self, order: Order):
        self.order = order

    def __str__(self):
        return f"Task: deliver {self.order.dish} to {self.order.customer}"
    
    def __repr__(self):
        return f"Task: deliver {self.order.dish} to {self.order.customer}"
    
class CollectBill(Task):
    def __init__(self, customer: Customer):
        self.customer = customer

    def __str__(self):
        return f"Task: collect the bill of {self.customer}"
    
    def __repr__(self):
        return f"Task: collect the bill of {self.customer}"
    
class ReturnToKitchen(Task):
    def __str__(self):
        return f"Task: return to the kitchen"
    
    def __repr__(self):
        return f"Task: return to the kitchen"