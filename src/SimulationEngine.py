import math
import random
from src.Restaurant import Restaurant
from src.events.EventQueue import EventQueue
from src.events.events import *
from src.agents.Customer import Customer
from src.agents.Waiter import Waiter
from src.Dish import Dish
from src.Table import Table
from src.tasks.tasks import *
from src.fuzzy_logic import FuzzyTip 

class SimulationEngine:
    def __init__(self, duration, arrival_rate, waiter_amount, verbose=False):
        self.duration = duration
        self.arrival_rate = arrival_rate
        self.waiter_amount = waiter_amount
        self.restaurant = None
        self.event_queue: EventQueue = EventQueue()
        self.current_time = 0
        self.verbose = verbose
        self.tipping = FuzzyTip()
        self.customers_waiting_queue = []
    
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

    def run(self, restaurant_grid, rules_priority):
        self.event_queue.clear()        # deberia estar vacia, pero x si acaso
        # print(restaurant_grid)
        self.restaurant = Restaurant(restaurant_grid, self.waiter_amount, rules_priority)
        self.generate_customer_arrivals(self.arrival_rate)

        while not self.event_queue.is_empty():
            event = self.event_queue.next_event()

            if self.verbose: 
                print("Time:", event.time, "Event:", type(event).__name__)
            
            self.current_time = event.time
            self.process_event(event)
            
        if self.verbose:
            print("Total tips:", self.restaurant.total_tips)
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
    
    def calc_dish_temperature(self, initial_temperature, room_temperature, time_passed):
        """Calculates the current temperature of a dish using Newton's Law of Cooling.

        Args:
            initial_temperature: The initial temperature of the dish in degrees Celsius.
            room_temperature: The temperature of the surrounding environment in degrees Celsius.
            time_passed: The time that has passed since the initial temperature was measured, in seconds.

        Returns:
            The current temperature of the dish in degrees Celsius.
        """
        # Converting time to minutes
        time_passed /= 60

        # Assuming a typical cooling constant for food
        cooling_constant = 0.09

        # Calculate the temperature difference between the initial temperature and room temperature
        temperature_difference = initial_temperature - room_temperature

        # Apply Newton's Law of Cooling formula
        current_temperature = room_temperature + temperature_difference * math.exp(-cooling_constant * time_passed)

        return current_temperature
    
    def get_tip_percentage(self, waiting_time, food_temp):
        return self.tipping.get_tip(waiting_time, food_temp)
    
    def get_tip(self, tip_percent, bill):
        return bill * tip_percent / 100

    def process_next_task(self, waiter: Waiter, place_id, time, verbose):
        # el camarero decide su acción
        waiter.decide_action(time, verbose)
        task = waiter.cur_task

        if isinstance(task, TakeDish):
            order = task.order
            for i in range(len(self.restaurant.kitchen.prepared_orders)):
                if order == self.restaurant.kitchen.prepared_orders[i]:
                    self.restaurant.kitchen.prepared_orders.pop(i)
                    break
            # toma el plato preparado de la cocina, termina esta tarea y busca otra
            waiter.add_dish(order, time, verbose)
            waiter.finish_cur_task(time, verbose)
            self.process_next_task(waiter, place_id, time, verbose)

        elif isinstance(task, TakeOrder):
            customer: Customer = task.customer
            path = self.restaurant.path_matrix[place_id][customer.table_id]
            waiter.start_walking(path, time, self.verbose)
            waiter.at_kitchen = False
            # crea un evento WaiterStartsTakingOrder
            self.event_queue.add_event(WaiterStartsTakingOrder(time + len(path) - 1, waiter, customer))
        
        elif isinstance(task, ReturnToKitchen):
            path = self.restaurant.path_matrix[place_id][self.restaurant.kitchen.id]
            waiter.start_walking(path, time, self.verbose)
            waiter.at_kitchen = True
            # crea un evento WaiterReturnsToKitchen
            self.event_queue.add_event(WaiterReturnsToKitchen(time + len(path) - 1, waiter))
        
        elif isinstance(task, DeliverDish):
            order: Order = task.order
            customer: Customer = order.customer
            path = self.restaurant.path_matrix[place_id][customer.table_id]
            waiter.at_kitchen = True
            waiter.start_walking(path, time, self.verbose)
            # crea un evento WaiterDeliversDish
            self.event_queue.add_event(WaiterDeliversDish(time + len(path) - 1, waiter, customer))
        
        elif isinstance(task, CollectBill):
            customer: Customer = task.customer
            path = self.restaurant.path_matrix[place_id][customer.table_id]
            waiter.start_walking(path, time, self.verbose)
            waiter.at_kitchen = True
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
                self.customers_waiting_queue.append(customer)

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

            # se le asigna el task de tomar la orden
            task = TakeOrder(customer)
            called_waiter_is_free = called_waiter.is_free()
            called_waiter.add_task(task, event.time, self.verbose)
            customer.start_waiting(event.time, self.verbose)

            # si el mesero no tiene nada que hacer
            if called_waiter_is_free:
                # debe estar en la cocina
                self.process_next_task(called_waiter, self.restaurant.kitchen.id, event.time, self.verbose)

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
            waiter.finish_cur_task(event.time, self.verbose)

            # añade la orden al inventario
            waiter.add_order(Order(dish, customer), event.time, self.verbose)

            # el cliente empieza a esperar por la comida
            customer.start_waiting(event.time, self.verbose)

            # procesa el siguiente task del mesero
            self.process_next_task(waiter, customer.table_id, event.time, self.verbose)
        
        elif isinstance(event, WaiterReturnsToKitchen) or isinstance(event, WaiterCleansTable):
            # Un mesero regresa a la cocina.
            waiter: Waiter = event.waiter
            waiter.stop_walking(event.time, self.verbose)
            waiter.at_kitchen = True
            waiter.dishes_at_kitchen = self.restaurant.kitchen.prepared_orders
            
            # termina esta encomienda
            waiter.finish_cur_task(event.time, self.verbose)
            
            # deja las órdenes que tenía en el inventario
            while len(waiter.orders_queue) > 0:
                order = waiter.orders_queue.pop(0)
                self.restaurant.kitchen.add_order(order, event.time, self.verbose)
                if self.restaurant.kitchen.has_capacity():
                    self.restaurant.kitchen.start_next_order(event.time, self.verbose)
                    cooking_time = order.dish.get_new_prob_cooking_time()
                    self.event_queue.add_event(KitchenPreparesOrder(event.time + cooking_time, order))
                    
            # procesa el siguiente task del mesero
            self.process_next_task(waiter, self.restaurant.kitchen.id, event.time, self.verbose)
        
        elif isinstance(event, KitchenPreparesOrder):
            # La cocina termina de preparar una orden.
            order: Order = event.order
            self.restaurant.kitchen.finish_order(order, event.time, self.verbose)
            if len(self.restaurant.kitchen.orders_queue) > 0:
                order = self.restaurant.kitchen.orders_queue[0]
                self.restaurant.kitchen.start_next_order(event.time, self.verbose)
                cooking_time = order.dish.get_new_prob_cooking_time()
                self.event_queue.add_event(KitchenPreparesOrder(event.time + cooking_time, order))
        
            for waiter in self.restaurant.waiters:
                if waiter.is_free():
                    self.process_next_task(waiter, self.restaurant.kitchen.id, event.time, self.verbose)
                    break
        
        elif isinstance(event, WaiterDeliversDish):
            # Un mesero llega a una mesa y le entrega el plato ordenado al cliente, 
            waiter: Waiter = event.waiter
            customer: Customer = event.customer

            waiter.stop_walking(event.time, self.verbose)
            customer.stop_waiting(event.time, self.verbose)
            task: DeliverDish = waiter.cur_task
            dish_served_temperature = self.calc_dish_temperature(task.order.initial_temperature, 25, event.time - task.order.preparation_time)
            customer.get_served(task.order, event.time, dish_served_temperature, self.verbose)

            waiter.finish_cur_task(event.time, self.verbose)
            self.process_next_task(waiter, customer.table_id, event.time, self.verbose)

            eating_time = random.randint(600, 1200) # config
            self.event_queue.add_event(CustomerFinishesEating(event.time + eating_time, customer))
        
        elif isinstance(event, CustomerFinishesEating):
            # Un cliente termina de comer y llama a un mesero para que recoja la cuenta.
            customer: Customer = event.customer

            # busca al mesero más cercano
            called_waiter = self.closest_waiter(customer.position, event.time)

            # se le asigna el task de cobrar la cuenta
            task = CollectBill(customer)
            called_waiter_is_free = called_waiter.is_free()
            called_waiter.add_task(task, event.time, self.verbose)
            customer.start_waiting(event.time, self.verbose)

            # si el mesero no tiene nada que hacer
            if called_waiter_is_free:
                # debe estar en la cocina
                self.process_next_task(called_waiter, self.restaurant.kitchen.id, event.time, self.verbose)

        elif isinstance(event, WaiterDeliversBill):
            # Un mesero llega a una mesa y le entrega la cuenta al cliente, el cual empieza a pagar
            waiter: Waiter = event.waiter
            customer: Customer = event.customer

            waiter.stop_walking(event.time, self.verbose)
            customer.stop_waiting(event.time, self.verbose)

            paying_time = random.randint(60, 180) # config
            # crea un evento CustomerPays
            self.event_queue.add_event(CustomerPays(event.time + paying_time, customer, waiter))

        elif isinstance(event, CustomerPays):
            # un cliente termina de pagarle a un mesero
            customer: Customer = event.customer
            waiter: Waiter = event.waiter

            # deja una propina
            tip_percent = self.get_tip_percentage(customer.total_wating_time, customer.dish_served_temperature)
            tip = self.get_tip(tip_percent, 20)
            customer.leave_tip(tip_percent, tip, event.time, self.verbose)
            self.restaurant.total_tips += tip

            # se levanta de la mesa y empieza a caminar hacia la salida
            customer_path = self.restaurant.path_matrix[customer.table_id][self.restaurant.entry_door.id]
            customer.start_walking(customer_path, event.time, self.verbose)

            # crea un evento CustomerLeaves
            self.event_queue.add_event(CustomerLeaves(event.time + len(customer_path) - 1, customer))

            # el mesero limpia la mesa y regresa con los platos y el pago a la cocina 
            waiter_path = self.restaurant.path_matrix[customer.table_id][self.restaurant.kitchen.id]
            waiter.start_walking(waiter_path, event.time, self.verbose)

            # crea un evento WaiterCleansTable
            self.event_queue.add_event(WaiterCleansTable(event.time + len(waiter_path) - 1, waiter))
        
        elif isinstance(event, CustomerLeaves):
            # Un cliente llega a la salida y se va del restaurante.
            customer: Customer = event.customer

            customer.stop_walking(event.time, self.verbose)
            table = self.restaurant.tables[customer.table_id - 2]
            table.is_available = True

            if len(self.customers_waiting_queue) > 0:
                customer = self.customers_waiting_queue.pop(0)
                table.is_available = False
                customer.table_id = table.id
                path = self.restaurant.path_matrix[self.restaurant.entry_door.id][table.id]
                customer.stop_waiting(event.time, self.verbose)
                customer.start_walking(path, event.time, self.verbose)
                self.event_queue.add_event(CustomerSits(event.time + len(path) - 1, customer))
