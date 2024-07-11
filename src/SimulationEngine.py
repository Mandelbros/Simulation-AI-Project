import random
from src.Restaurant import Restaurant
from src.events.EventQueue import EventQueue
from src.events.events import *
from src.agents.Customer import Customer
from src.Table import Table
from random import randint

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
        customer_id = 1

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
            decision_time = randint(10,300)  # config

            # crea un evento CustomerOrders
            self.event_queue.add_event(CustomerOrders(event.time + decision_time, customer))

        elif isinstance(event, CustomerOrders):
            # Un cliente decide qué ordenar y llama a un mesero
            customer: Customer = event.customer
            customer.start_waiting(event.time, self.verbose)

            best_dist = 100000000000
            for waiter in self.restaurant.waiters:
                # calcula la distancia del cliente al mesero
                dist = customer.position.euclidean_dist_to(waiter.get_position_at(event.time))
                # se queda con el mesero más cercano (con distancia euclidiana)
                if best_dist > dist:
                    best_dist = dist
                    called_waiter = waiter

            if len(called_waiter.dests_queue) == 0: # si el mesero no tiene nada que hacer
                # debe estar en la cocina, desde la que empieza a caminar hacia la mesa del cliente
                path = self.restaurant.path_matrix[self.restaurant.kitchen.id][customer.table_id]
                called_waiter.start_walking(path, event.time, self.verbose)
                # crea un evento WaiterStartsTakingOrder
                self.event_queue.add_event(WaiterStartsTakingOrder(event.time + len(path) - 1, called_waiter, customer))
            called_waiter.add_dest(customer.table_id)

        elif isinstance(event, WaiterStartsTakingOrder):
            # Un mesero llega a una mesa 
            customer: Customer = event.customer
            waiter: Waiter = event.waiter
            waiter.stop_walking(event.time, self.verbose)

            # y empieza a tomar una orden de un cliente 
            customer.stop_waiting(event.time, self.verbose)
            ordering_time = randint(60, 300) # config

            # crea un evento WaiterTakesOrder.
            self.event_queue.add_event(WaiterTakesOrder(event.time + ordering_time, waiter, customer))
        # ...