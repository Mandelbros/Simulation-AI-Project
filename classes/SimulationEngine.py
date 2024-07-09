class SimulationEngine:
    def __init__(self, restaurant, event_queue, duration):
        self.restaurant = restaurant
        self.event_queue = event_queue
        self.current_time = 0
        self.duration = duration

    def run(self):
        while self.current_time < self.duration:
            event = self.event_queue.next_event()
            if event:
                self.current_time = event.time
                if self.current_time > self.duration:
                    break  # Stop the simulation if it exceeds the specified duration
                self.restaurant.process_event(event)
            else:
                break  # No more events to process