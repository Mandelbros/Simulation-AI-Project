from typing import List
from enum import Enum, auto
from src.events.events import Event, CustomerArrives
from src.utils.utils import Place, Position
from src.Kitchen import Kitchen
from src.agents.Waiter import Waiter
from src.Table import Table

class PlaceType(Enum):
    WALL = auto()
    FLOOR = auto()
    TABLE = auto()
    KITCHEN = auto()
    ENTRY_DOOR = auto()

class Restaurant: 
    def __init__(self, restaurant_grid, waiter_amount):
        self.restaurant_grid = restaurant_grid
        self.waiter_amount = waiter_amount
        self.total_tips = 0  # Add total_tips attribute
        self.path_matrix = None
        self.entry_door_position: Place = None
        self.kitchen = None
        self.tables = [] 
        self.waiters = [Waiter(i) for i in range(waiter_amount)]
        self.init_places()
        self.fill_path_matrix()

    def init_places(self): 
        """
        This method initializes the places in the restaurant. It iterates over the restaurant grid and for each cell, 
        if it's an entry door (4), it sets the entry door position. If it's a kitchen (3), it creates a new Place 
        object for the kitchen. If it's a table (2), it creates a new Place object for the table and adds it to the tables list.

        Parameters:
        None

        Returns:
        None
        """
        for i, row in enumerate(self.restaurant_grid):
            for j, cell in enumerate(row):
                position = Position(i, j)
                if cell == PlaceType.ENTRY_DOOR:
                    self.entry_door_position = Place(0, position)
                elif cell == PlaceType.KITCHEN:
                    self.kitchen = Kitchen(1, position)
                elif cell == PlaceType.TABLE:
                    self.tables.append(Table(len(self.tables) + 2, position))

    def get_path(self, start_position: Position, end_position: Position):
        """
        This method finds the shortest path from the start position to the end position.

        Parameters:
        start_position (Position): The start position.
        end_position (Position): The end position.

        Returns:
        List[Position]: The shortest path from the start position to the end position, or None if there's no path.
        """
        queue = [start_position]
        visited = {start_position}
        path = {start_position: []}

        while queue:
            position = queue.pop(0)
            if position == end_position:
                return path[position]

            for dr, dc in [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]:
                row, col = position.row + dr, position.col + dc
                if 0 <= row < len(self.restaurant_grid) and 0 <= col < len(self.restaurant_grid[0]):
                    next_position = Position(row, col)
                    if next_position not in visited and (self.restaurant_grid[row][col] == PlaceType.FLOOR or next_position == end_position):
                        queue.append(next_position)
                        visited.add(next_position)
                        path[next_position] = path[position] + [next_position]

        return None  # Return None if there's no path

    def fill_path_matrix(self):
        """
        This method fills the path matrix, which is a 2D list where the cell at the i-th row and j-th column 
        contains the shortest path from the i-th place to the j-th place. It first initializes the path matrix 
        with None values, then for each pair of places, it uses the get_path method to find the shortest path 
        between them and stores it in the corresponding cell of the path matrix.

        Parameters:
        None

        Returns:
        None
        """
        places: List[Place] = [self.entry_door_position, self.kitchen] + self.tables
        self.path_matrix = [[None for _ in places] for _ in places]
        for i, start in enumerate(places):
            for j, end in enumerate(places):
                if i!=j:
                    self.path_matrix[i][j] = self.get_path(start.position, end.position)

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
