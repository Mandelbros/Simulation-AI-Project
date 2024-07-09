import Restaurant
class SimulationEngine:
    def __init__(self, duration, restaurant_grid, table_amount, waiter_amount):
        self.duration = duration
        self.restaurant = Restaurant(restaurant_grid, table_amount, waiter_amount)
        self.event_queue = metodo()
        self.current_time = 0

    def run(self):
        while self.current_time < self.duration:
            event = self.event_queue.next_event()
            if event:
                self.current_time = event.time
                self.restaurant.process_event(event)
            else:
                break  # No more events to process
        return self.restaurant.total_tips  # Return the total tips collected during the simulation