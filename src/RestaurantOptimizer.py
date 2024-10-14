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
        self.empty_positions = []
        self.tables_positions = []
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
    
    def get_neighbour(self, optimize_grid=False, optimize_rules=False):
        new_grid = [row[:] for row in self.layout_grid] 
        new_rules = self.rules_priority[:]

        if optimize_grid:
            tables = self.tables_positions[:]
            random.shuffle(tables)

            for table in tables:
                dirs = [(-1,-1), (-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
                random.shuffle(dirs)

                new_grid[table[0]][table[1]] = PlaceType.FLOOR

                for dir in dirs:
                    nr = table[0]+dir[0]
                    nc = table[1]+dir[1]

                    if self.is_available_pos(new_grid, nr,nc):
                        new_grid[nr][nc]=PlaceType.TABLE
                        return new_rules, new_grid, (table[0], table[1]), (nr, nc)
                        
                
                new_grid[table[0]][table[1]]=PlaceType.TABLE

        if optimize_rules:
            rule1 = random.randint(0, len(new_rules) - 1)
            rule2 = random.randint(0, len(new_rules) - 2)

            if rule2>=rule1:
                rule2+=1

            new_rules[rule1], new_rules[rule2] = new_rules[rule2], new_rules[rule1]

        return new_rules, new_grid, (0,0), (0,0)

    
    def is_available_pos(self, grid, r, c):
        if grid[r][c] != PlaceType.FLOOR:
            return False
        
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr==0 and dc==0:
                    continue

                nr, nc = r + dr, c + dc

                if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] not in (PlaceType.WALL, PlaceType.FLOOR):
                    return False
                
        return True

    def add_table(self, r, c):
        self.layout_grid[r][c] = PlaceType.TABLE
        self.tables_positions.append((r, c))

    def remove_table(self, r, c):
        self.layout_grid[r][c] = PlaceType.FLOOR
        self.tables_positions.remove((r, c))

    def cost_function(self, layout_grid, rules_priority):
        total_tips = 0
        total_waiting_time = 0
        for _ in range(self.nights_per_layout):
            nigth_tips, nigth_waiting_time = self.simulation_engine.run(layout_grid, rules_priority)
            total_tips += nigth_tips
            total_waiting_time += nigth_waiting_time

        return -total_tips / self.nights_per_layout, total_waiting_time / self.nights_per_layout
    
    def simulated_annealing(self, optimize_grid=True, optimize_rules=False):
        current_cost, best_waiting_time = self.cost_function(self.layout_grid, self.rules_priority)
        best_config = self.layout_grid
        best_cost = current_cost
        init_tips = -best_cost     ##
        init_wait = best_waiting_time  ##
        
        temp = self.initial_temp

        while temp > self.final_temp:
            for _ in range(self.max_iter):
                neighbour_rules,neighbour_layout, table_pos, empty_pos = self.get_neighbour(optimize_grid, optimize_rules)

                neighbour_cost, current_waiting_time = self.cost_function(neighbour_layout, neighbour_rules)
                delta_cost = neighbour_cost - current_cost

                for row in self.layout_grid:
                    for cell in row:
                        if cell == 0:
                            print("#", end="")
                        elif cell == 1:
                            print(".",end="")
                        elif cell == 2:
                            print("O",end="")
                        elif cell == 3:
                            print("C",end="")
                        elif cell == 4:
                            print("P",end="")
                    print()
                print("temp: ", temp)
                print(math.exp(-delta_cost / temp))
                print("best cost: ", best_cost)
                print("cost: ", current_cost)
                print("")

                if delta_cost < 0 or random.uniform(0, 1) < math.exp(-delta_cost / temp):
                    current_cost = neighbour_cost

                    if optimize_grid:
                        self.layout_grid = neighbour_layout
                        self.remove_table( table_pos[0], table_pos[1])
                        self.add_table( empty_pos[0], empty_pos[1])
                    if optimize_rules:
                        self.rules_priority = neighbour_rules

                    if current_cost < best_cost:
                        best_config = self.layout_grid
                        best_cost = current_cost
                        best_waiting_time = current_waiting_time
                        # print(self.rules_priority)

            temp *= self.alpha

        return best_config, -best_cost, best_waiting_time, init_tips, init_wait
