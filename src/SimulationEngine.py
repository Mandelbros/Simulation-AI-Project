import random
from src.Restaurant import Restaurant
from src.events.EventQueue import EventQueue
from src.events.events import *
from src.agents.Customer import Customer
from src.agents.Waiter import Waiter
from src.Dish import Dish
from src.Table import Table
from src.requests.requests import *

class SimulationEngine:
    def __init__(self, duration, lambda_rate, restaurant_grid, waiter_amount, verbose=False):
        self.duration = duration
        self.restaurant: Restaurant = Restaurant(restaurant_grid, waiter_amount)
        self.event_queue: EventQueue = EventQueue()
        self.current_time = 0
        self.verbose = verbose
        self.generate_customer_arrivals(lambda_rate)
    
    def generate_customer_arrivals(self, lambda_rate):
        """
        This method generates customer arrival events based on a Poisson process.
        The inter-arrival times are exponentially distributed with a rate parameter `lambda_rate`.
        Each customer is assigned a unique ID and an arrival event is created and added to the event queue.
        
        Parameters:
        lambda_rate (float): The rate parameter for the exponential distribution used to generate inter-arrival times.
        
        Returns:
        None
        """
        current_time = 0
        customer_id = 0

        while current_time < self.duration:
            inter_arrival_time = round(random.expovariate(lambda_rate))
            current_time += inter_arrival_time
            if current_time < self.duration:
                customer = Customer(customer_id, self.restaurant.entry_door.position)
                customer_id += 1
                arrival_event = CustomerArrives(current_time, customer)
                self.event_queue.add_event(arrival_event)

    def run(self):
        while not self.event_queue.is_empty():
            event = self.event_queue.next_event()

            if self.verbose: 
                print("Time:", event.time, "Event:", type(event).__name__)
            
            self.current_time = event.time
            self.process_event(event)
            
        return self.restaurant.total_tips  # Return the total tips collected during the simulation
    
    def closest_waiter(self, position, time):
        best_dist = 100000000000
        for waiter in self.restaurant.waiters:
            # calcula la distancia de la posición al mesero
            dist = position.euclidean_dist_to(waiter.get_position_at(time))
            # se queda con el mesero más cercano (con distancia euclidiana)
            if best_dist > dist:
                best_dist = dist
                called_waiter = waiter
        return called_waiter

    def process_next_request(self, waiter: Waiter, place_id, time):
        if waiter.is_free():
            # si no tiene nada que hacer, regresa a la cocina
            waiter.add_request(ReturnToKitchen(), time, self.verbose)
            self.process_next_request(waiter, place_id, time)
        else:
            # en caso contrario, procesa el siguiente request
            request = waiter.next_request()

            if isinstance(request, TakeOrder):
                customer: Customer = request.customer
                path = self.restaurant.path_matrix[place_id][customer.table_id]
                waiter.start_walking(path, time, self.verbose)
                # crea un evento WaiterStartsTakingOrder
                self.event_queue.add_event(WaiterStartsTakingOrder(time + len(path) - 1, waiter, customer))
            
            elif isinstance(request, ReturnToKitchen):
                path = self.restaurant.path_matrix[place_id][self.restaurant.kitchen.id]
                waiter.start_walking(path, time, self.verbose)
                # crea un evento WaiterReturnsToKitchen
                self.event_queue.add_event(WaiterReturnsToKitchen(time + len(path) - 1, waiter))
            
            elif isinstance(request, DeliverDish):
                order: Order = request.order
                customer: Customer = order.customer
                path = self.restaurant.path_matrix[place_id][customer.table_id]
                waiter.start_walking(path, time, self.verbose)
                # crea un evento WaiterDeliversDish
                self.event_queue.add_event(WaiterDeliversDish(time + len(path) - 1, waiter, customer))
            
            elif isinstance(request, CollectBill):
                customer: Customer = request.customer
                path = self.restaurant.path_matrix[place_id][customer.table_id]
                waiter.start_walking(path, time, self.verbose)
                # crea un evento WaiterDeliversBill
                self.event_queue.add_event(WaiterDeliversBill(time + len(path) - 1, waiter, customer))

    def process_event(self, event: Event):
        if isinstance(event, CustomerArrives):
            # Llega un cliente al restaurante
            customer: Customer = event.customer
            table: Table = self.restaurant.get_available_table()

            if table is not None:
                # si hay mesa libre empieza a caminar hacia ella (crea un evento CustomerSits), 
                table.is_available = False
                customer.table_id = table.id
                path = self.restaurant.path_matrix[self.restaurant.entry_door.id][table.id]
                customer.start_walking(path, event.time, self.verbose)
                self.event_queue.add_event(CustomerSits(event.time + len(path) - 1, customer))
            else:
                # si no espera hasta que se desocupe una mesa (en algún evento CustomerLeaves)
                customer.start_waiting(event.time, self.verbose)
                path = None

        elif isinstance(event, CustomerSits):
            # Un cliente termina de caminar, se sienta en una mesa
            customer: Customer = event.customer
            customer.stop_walking(event.time, self.verbose)

            # y empieza a pensar en qué ordenar
            decision_time = random.randint(10,300)  # config

            # crea un evento CustomerOrders
            self.event_queue.add_event(CustomerOrders(event.time + decision_time, customer))

        elif isinstance(event, CustomerOrders):
            # Un cliente decide qué ordenar y llama a un mesero
            customer: Customer = event.customer

            # busca al mesero más cercano
            called_waiter = self.closest_waiter(customer.position, event.time)

            # se le asigna el request de tomar la orden
            request = TakeOrder(customer)
            called_waiter_is_free = called_waiter.is_free()
            called_waiter.add_request(request, event.time, self.verbose)
            customer.start_waiting(event.time, self.verbose)

            # si el mesero no tiene nada que hacer
            if called_waiter_is_free:
                # debe estar en la cocina
                self.process_next_request(called_waiter, self.restaurant.kitchen.id, event.time)

        elif isinstance(event, WaiterStartsTakingOrder):
            # Un mesero llega a una mesa 
            customer: Customer = event.customer
            waiter: Waiter = event.waiter
            waiter.stop_walking(event.time, self.verbose)

            # y empieza a tomar una orden de un cliente 
            customer.stop_waiting(event.time, self.verbose)
            dish = self.restaurant.dishes[0]
            ordering_time = random.randint(60, 300) # config

            # crea un evento WaiterTakesOrder.
            self.event_queue.add_event(WaiterTakesOrder(event.time + ordering_time, waiter, customer, dish))

        elif isinstance(event, WaiterTakesOrder):
            # Un mesero termina de tomar una orden de un cliente.
            customer: Customer = event.customer
            waiter: Waiter = event.waiter
            dish: Dish = event.dish

            # termina esta encomienda
            waiter.finish_next_request(event.time, self.verbose)

            # añade la orden al inventario
            waiter.add_order(Order(dish, customer), event.time, self.verbose)

            # el cliente empieza a esperar por la comida
            customer.start_waiting(event.time, self.verbose)

            # procesa el siguiente request del mesero
            self.process_next_request(waiter, customer.table_id, event.time)
        
        elif isinstance(event, WaiterReturnsToKitchen):
            # Un mesero regresa a la cocina.
            waiter: Waiter = event.waiter
            waiter.stop_walking(event.time, self.verbose)
            
            # termina esta encomienda
            waiter.finish_next_request(event.time, self.verbose)
            
            # deja las órdenes que tenía en el inventario
            while len(waiter.orders_queue) > 0:
                order = waiter.orders_queue.pop(0)
                self.restaurant.kitchen.add_order(order, event.time, self.verbose)
                if self.restaurant.kitchen.has_capacity():
                    self.restaurant.kitchen.start_next_order(event.time, self.verbose)
                    cooking_time = order.dish.get_new_prob_cooking_time()
                    self.event_queue.add_event(KitchenPreparesOrder(event.time + cooking_time, order))

            # recoge las órdenes preparadas que pueda
            while len(self.restaurant.kitchen.prepared_orders) > 0 and waiter.has_capacity():
                order = self.restaurant.kitchen.take_next_prepared_order()
                request = DeliverDish(order)
                waiter.add_dish(order, event.time, self.verbose)
                waiter.add_request(request, event.time, self.verbose)

            # procesa el siguiente request del mesero
            if not waiter.is_free():
                self.process_next_request(waiter, self.restaurant.kitchen.id, event.time)
        
        elif isinstance(event, KitchenPreparesOrder):
            # La cocina termina de preparar una orden.
            order: Order = event.order
            self.restaurant.kitchen.finish_order(order, event.time, self.verbose)
        
            for waiter in self.restaurant.waiters:
                if waiter.is_free():
                    order = self.restaurant.kitchen.take_next_prepared_order()
                    request = DeliverDish(order)
                    waiter.add_dish(order, event.time, self.verbose)
                    waiter.add_request(request, event.time, self.verbose)
                    self.process_next_request(waiter, self.restaurant.kitchen.id, event.time)
                    break
        
        elif isinstance(event, WaiterDeliversDish):
            # Un mesero llega a una mesa y le entrega el plato ordenado al cliente, 
            waiter: Waiter = event.waiter
            customer: Customer = event.customer

            waiter.stop_walking(event.time, self.verbose)
            customer.stop_waiting(event.time, self.verbose)

            waiter.finish_next_request(event.time, self.verbose)
            self.process_next_request(waiter, customer.table_id, event.time)

            eating_time = random.randint(600, 1200) # config
            self.event_queue.add_event(CustomerFinishesEating(event.time + eating_time, customer))
        
        elif isinstance(event, CustomerFinishesEating):
            # Un cliente termina de comer y llama a un mesero para que recoja la cuenta.
            customer: Customer = event.customer

            # busca al mesero más cercano
            called_waiter = self.closest_waiter(customer.position, event.time)

            # se le asigna el request de cobrar la cuenta
            request = CollectBill(customer)
            called_waiter_is_free = called_waiter.is_free()
            called_waiter.add_request(request, event.time, self.verbose)
            customer.start_waiting(event.time, self.verbose)

            # si el mesero no tiene nada que hacer
            if called_waiter_is_free:
                # debe estar en la cocina
                self.process_next_request(called_waiter, self.restaurant.kitchen.id, event.time)

        elif isinstance(event, WaiterDeliversBill):
            # Un mesero llega a una mesa y le entrega la cuenta al cliente, el cual empieza a pagar
            waiter: Waiter = event.waiter
            customer: Customer = event.customer

            waiter.stop_walking(event.time, self.verbose)
            customer.stop_waiting(event.time, self.verbose)

            paying_time = random.randint(60, 180) # config
            # crea un evento CustomerPays
            self.event_queue.add_event(CustomerPays(event.time + paying_time, customer, waiter))
        # ...
