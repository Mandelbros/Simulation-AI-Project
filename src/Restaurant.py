from src.events.events import Event, CustomerArrives

class Restaurant: 
    def __init__(self, restaurant_grid, table_amount, waiter_amount):
        # self.tables = [Table(i) for i in range(num_tables)]
        # self.waiters = [Waiter(i) for i in range(num_waiters)]
        # self.kitchen = Kitchen()
        self.restaurant_grid = restaurant_grid
        self.table_amount = table_amount
        self.waiter_amount = waiter_amount
        self.total_tips = 0  # Add total_tips attribute

    # def add_customer(self, customer, arrival_time):
    #     self.customers.append(customer)
    #     event = Event(arrival_time, 'CustomerArrives', customer)
    #     self.event_queue.add_event(event)

    def process_event(self, event:Event):
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
