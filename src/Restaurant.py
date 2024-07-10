from src.events.events import Event, CustomerArrives
from src.utils.utils import Position
from src.Kitchen import Kitchen
from src.agents.Waiter import Waiter

class Restaurant: 
    def __init__(self, restaurant_grid, waiter_amount):
        self.restaurant_grid = restaurant_grid
        self.waiter_amount = waiter_amount
        self.total_tips = 0  # Add total_tips attribute
        self.path_matrix = None
        self.entry_door_position: Position = None
        self.kitchen = None
        self.tables = None 
        self.waiters = [Waiter(i) for i in range(waiter_amount)]
        self.init_places()
        self.fill_path_matrix()

    def init_places():
        pass

    def get_path(self, start_position: Position, end_position: Position):
        # Implement your pathfinding algorithm here
        pass

    def fill_path_matrix(self):
        pass

    def process_event(self, event: Event):
        if isinstance(event, CustomerArrives):
            pass
            # self.assign_table(event.customer)


        # elif event.event_type == 'CustomerOrder':
        #     waiter = self.find_idle_waiter()
        #     if waiter:
        #         waiter.take_order(event.customer)
        #         food_ready_time = event.time + event.customer.order_time
        #         self.event_queue.add_event(Event(food_ready_time, 'OrderReady', event.customer, waiter))
        # elif event.event_type == 'OrderReady':
        #     event.waiter.serve_food(event.customer)
        #     eat_time = event.time + event.customer.eat_time
        #     self.event_queue.add_event(Event(eat_time, 'CustomerEat', event.customer))
        # elif event.event_type == 'CustomerEat':
        #     event.customer.eat()
        #     bill_request_time = event.time + event.customer.eat_time
        #     self.event_queue.add_event(Event(bill_request_time, 'CustomerRequestBill', event.customer))
        # elif event.event_type == 'CustomerRequestBill':
        #     waiter = self.find_idle_waiter()
        #     if waiter:
        #         waiter.give_bill(event.customer)
        #         bill_wait_time = event.time + event.customer.bill_wait_time
        #         self.event_queue.add_event(Event(bill_wait_time, 'CustomerPayAndLeave', event.customer, waiter))
        # elif event.event_type == 'CustomerPayAndLeave':
        #     event.customer.pay_and_leave()
        #     self.total_tips += event.customer.tip  # Update total_tips when a customer pays and leaves
        #     self.cleanup(event.customer)

    # def assign_table(self, customer):
    #     for table in self.tables:
    #         if not table.is_occupied:
    #             table.occupy(customer)
    #             customer.table = table
    #             customer_think_time = random_time()
    #             self.event_queue.add_event(Event(customer_think_time, 'CustomerOrder', customer))
    #             return

    # def find_idle_waiter(self):
    #     for waiter in self.waiters:
    #         if waiter.state == 'idle':
    #             return waiter
    #     return None

    # def cleanup(self, customer):
    #     customer.table.vacate()
    #     self.customers.remove(customer)
