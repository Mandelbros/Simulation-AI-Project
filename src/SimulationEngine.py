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
            customer: Customer = event.customer
            table: Table = self.restaurant.get_available_table()
            if table is None:
                customer.start_waiting(event.time)
            else:
                table.is_available = False
                path = self.restaurant.path_matrix[self.restaurant.entry_door.id][table.id]
                customer.start_waiting(event.time)
                self.event_queue.add_event(CustomerSits(event.time + len(path) - 1, customer))
        elif isinstance(event, CustomerSits):
            customer: Customer = event.customer
            decision_time = randint(10,300)  # config
            self.event_queue.add_event(CustomerOrders(event.time + decision_time, customer))
        # ...