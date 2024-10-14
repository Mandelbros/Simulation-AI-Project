import random
import math
from src.SimulationEngine import SimulationEngine
from src.utils.utils import PlaceType  

class RestaurantOptimizer:
    def __init__(self, simulation_engine, initial_temp, final_temp, alpha, max_iter, nights_per_layout, initial_grid, num_tables, rules_priority, verbose=False):
        self.simulation_engine:SimulationEngine = simulation_engine
        self.initial_temp = initial_temp
        self.final_temp = final_temp
        self.alpha = alpha
        self.max_iter = max_iter
        self.nights_per_layout = nights_per_layout
        self.tables_positions = []
        self.empty_positions = []
        self.layout_grid = initial_grid
        self.rules_priority = rules_priority
        self.verbose = verbose
        self.fill_initial_grid(num_tables) 

    def fill_initial_grid(self, num_tables):
        rows, cols = len(self.layout_grid), len(self.layout_grid[0]) 

        available_positions = [[1 for _ in range(cols)] for _ in range(rows)] 

        for row in range(rows):
            for col in range(cols):
                cell = self.layout_grid[row][col]

                if cell == PlaceType.WALL:
                    available_positions[row][col] = 0
                elif cell in (PlaceType.TABLE, PlaceType.ENTRY_DOOR, PlaceType.KITCHEN):
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            nr, nc = row + dr, col + dc
                            if 0 <= nr < rows and 0 <= nc < cols:
                                available_positions[nr][nc] = 0

                    if cell == PlaceType.TABLE:
                        self.tables_positions.append((row, col))

        for row in range(rows):
            for col in range(cols):
                if available_positions[row][col]:
                    self.empty_positions.append((row, col))  
 
        while len(self.tables_positions) < num_tables:
            r, c = random.choice(self.empty_positions) 
            self.add_table(r, c)
    
    def get_neighbour(self):
        new_grid = [row[:] for row in self.layout_grid] 
        new_rules = self.rules_priority[:]

        empty_r, empty_c = random.choice(self.empty_positions) 
        table_r, table_c = random.choice(self.tables_positions) 

        new_grid[empty_r][empty_c] = PlaceType.TABLE
        new_grid[table_r][table_c] = PlaceType.FLOOR

        # rule1 = random.randint(0, len(new_rules) - 1)
        # rule2 = random.randint(0, len(new_rules) - 2)

        # if rule2>=rule1:
        #     rule2+=1

        # new_rules[rule1], new_rules[rule2] = new_rules[rule2], new_rules[rule1]
        return new_grid, new_rules, (table_r, table_c), (empty_r, empty_c)
    
    def is_available_pos(self, r, c):
        if self.layout_grid[r][c] != PlaceType.FLOOR:
            return False
        
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr==0 and dc==0:
                    continue

                nr, nc = r + dr, c + dc

                if 0 <= nr < len(self.layout_grid) and 0 <= nc < len(self.layout_grid[0]) and self.layout_grid[nr][nc] not in (PlaceType.WALL, PlaceType.FLOOR):
                    return False
                
        return True

    def add_table(self, r, c):
        self.layout_grid[r][c] = PlaceType.TABLE
        self.tables_positions.append((r, c))

        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = r + dr, c + dc

                if (nr, nc) in self.empty_positions:
                    self.empty_positions.remove((nr, nc))

    def remove_table(self, r, c):
        self.layout_grid[r][c] = PlaceType.FLOOR
        self.tables_positions.remove((r, c))

        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = r + dr, c + dc

                if self.is_available_pos(nr, nc):
                    self.empty_positions.append((nr, nc))

    def cost_function(self, layout_grid, rules_priority):
        total_tips = 0
        for _ in range(self.nights_per_layout):
            total_tips += self.simulation_engine.run(layout_grid, rules_priority)
        return -total_tips / self.nights_per_layout
    
    def simulated_annealing(self):
        current_cost = self.cost_function(self.layout_grid, self.rules_priority)
        best_config = self.layout_grid
        best_cost = current_cost
        temp = self.initial_temp

        while temp > self.final_temp:
            for _ in range(self.max_iter):
                neighbour_layout, neighbour_rules, table_pos, empty_pos = self.get_neighbour()

                neighbour_cost = self.cost_function(neighbour_layout, neighbour_rules)
                delta_cost = neighbour_cost - current_cost

                if delta_cost < 0 or random.uniform(0, 1) < math.exp(-delta_cost / temp):
                    self.layout_grid = neighbour_layout
                    self.rules_priority = neighbour_rules
                    current_cost = neighbour_cost


                    self.add_table(empty_pos[0], empty_pos[1])
                    self.remove_table(table_pos[0], table_pos[1])

                    if current_cost < best_cost:
                        best_config = self.layout_grid
                        best_cost = current_cost

                        # for row in self.layout_grid:
                        #     print(row)
                        # print("cost: ", best_cost)
                        # print("")

            temp *= self.alpha

        return best_config, -best_cost
