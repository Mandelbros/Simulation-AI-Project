import random
from src.Restaurant import Restaurant
from src.events.EventQueue import EventQueue
from src.events.events import CustomerArrives
from src.agents.Customer import Customer

class SimulationEngine:
    def __init__(self, duration, lambda_rate, restaurant_grid, table_amount, waiter_amount, verbose=False):
        self.duration = duration
        self.restaurant:Restaurant = Restaurant(restaurant_grid, table_amount, waiter_amount)
        self.event_queue:EventQueue = EventQueue()
        self.current_time = 0
        self.verbose = verbose
        self.generate_customer_arrivals(lambda_rate)
    
    def generate_customer_arrivals(self, lambda_rate):
        current_time = 0
        customer_id = 1

        while current_time < self.duration:
            inter_arrival_time = random.expovariate(lambda_rate)
            current_time += inter_arrival_time
            if current_time < self.duration:
                customer = Customer(customer_id)
                customer_id += 1
                arrival_event = CustomerArrives(current_time, customer)
                self.event_queue.add_event(arrival_event)

    def run(self):
        while not self.event_queue.is_empty():
            event = self.event_queue.next_event()

            if self.verbose: 
                print("Time:", event.time, "Event:", type(event).__name__)
            
            self.current_time = event.time
            self.restaurant.process_event(event)
            
        return self.restaurant.total_tips  # Return the total tips collected during the simulation