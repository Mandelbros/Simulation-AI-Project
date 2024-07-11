from src.agents.Customer import Customer
from src.Order import Order

class Request:
    pass
    
class TakeOrder(Request):
    def __init__(self, customer: Customer):
        self.customer = customer

    def __str__(self):
        return f"Request: take order of {self.customer}"
    
    def __repr__(self):
        return f"Request: take order of {self.customer}"
    
class DeliverDish(Request):
    def __init__(self, order: Order):
        self.order = order

    def __str__(self):
        return f"Request: deliver {self.order.dish} to {self.order.customer}"
    
    def __repr__(self):
        return f"Request: deliver {self.order.dish} to {self.order.customer}"
    
class CollectBill(Request):
    def __init__(self, customer: Customer):
        self.customer = customer

    def __str__(self):
        return f"Request: collect the bill of {self.customer}"
    
    def __repr__(self):
        return f"Request: collect the bill of {self.customer}"
    
class ReturnToKitchen(Request):
    def __str__(self):
        return f"Request: return to the kitchen"
    
    def __repr__(self):
        return f"Request: return to the kitchen"