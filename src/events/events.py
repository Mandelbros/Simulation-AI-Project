from src.agents.Customer import Customer
from src.agents.Waiter import Waiter
from src.Dish import Dish
from src.Order import Order

class Event:
    def __init__(self, time):
        self.time = time

    def __lt__(self, other: 'Event'):
        return self.time < other.time

class CustomerArrives(Event):
    """
        Llega un cliente al restaurante y si hay mesa libre empieza a caminar hacia ella (crea un CustomerSits), 
        si no espera hasta que se desocupe una mesa (en algún evento CustomerLeaves)
    """
    def __init__(self, time, customer: Customer):
        super().__init__(time)
        self.customer = customer

class CustomerSits(Event):
    """
        Un cliente termina de caminar, se sienta en una mesa y empieza a pensar en qué ordenar (crea un evento CustomerOrders).
    """
    def __init__(self, time, customer: Customer):
        super().__init__(time)
        self.customer = customer

class CustomerOrders(Event):
    """
        Un cliente decide qué ordenar y llama a un mesero.
    """
    def __init__(self, time, customer: Customer):
        super().__init__(time)
        self.customer = customer

class WaiterStartsTakingOrder(Event):
    """
        Un mesero llega a una mesa y empieza a tomar una orden de un cliente (crea un evento WaiterTakesOrder).
    """
    def __init__(self, time, waiter: Waiter, customer: Customer):
        super().__init__(time)
        self.waiter = waiter
        self.customer = customer

class WaiterTakesOrder(Event):
    """
        Un mesero termina de tomar una orden de un cliente.
    """
    def __init__(self, time, waiter: Waiter, customer: Customer, dish: Dish):
        super().__init__(time)
        self.waiter = waiter
        self.customer = customer
        self.dish = dish

class WaiterDeliversDish(Event):
    """
        Un mesero llega a una mesa y le entrega el plato ordenado al cliente, 
        el cual empieza a comer (crea un evento CustomerFinishesEating).
    """
    def __init__(self, time, waiter: Waiter, customer: Customer):
        super().__init__(time)
        self.waiter = waiter
        self.customer = customer

class CustomerFinishesEating(Event):
    """
        Un cliente termina de comer y llama a un mesero para que recoja la cuenta.
    """
    def __init__(self, time, customer: Customer):
        super().__init__(time)
        self.customer = customer

class WaiterDeliversBill(Event):
    """
        Un mesero llega a una mesa y le entrega la cuenta al cliente, 
        el cual empieza a pagar (crea un evento CustomerPays).
    """
    def __init__(self, time, waiter: Waiter, customer: Customer):
        super().__init__(time)
        self.waiter = waiter
        self.customer = customer

class CustomerPays(Event):
    """
        Un cliente termina de pagarle a un mesero, deja una propina, se levanta de la mesa 
        y empieza a caminar hacia la salida (crea un evento CustomerLeaves)
        y el mesero limpia la mesa y regresa con los platos y el pago a la cocina 
        (crea un evento WaiterCleansTable).
    """
    def __init__(self, time, customer: Customer, waiter: Waiter):
        super().__init__(time)
        self.customer = customer
        self.waiter = waiter

class WaiterCleansTable(Event):
    """
        Un mesero regresar a la cocina y deja los platos y la cuenta pagada
    """
    def __init__(self, time, waiter: Waiter):
        super().__init__(time)
        self.waiter = waiter

class WaiterReturnsToKitchen(Event):
    """
        Un mesero regresa a la cocina.
    """
    def __init__(self, time, waiter: Waiter):
        super().__init__(time)
        self.waiter = waiter

class CustomerLeaves(Event):
    """
        Un cliente llega a la salida y se va del restaurante.
    """
    def __init__(self, time, customer: Customer):
        super().__init__(time)
        self.customer = customer

class KitchenPreparesOrder(Event):
    """
        La cocina termina de preparar una orden.
    """
    def __init__(self, time, order: Order):
        super().__init__(time)
        self.order = order