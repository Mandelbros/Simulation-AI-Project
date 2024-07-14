import random
import math
from src.SimulationEngine import SimulationEngine
from src.utils.utils import PlaceType  

class RestaurantOptimizer:
    def __init__(self, simulation_engine, initial_temp, final_temp, alpha, max_iter, nights_per_layout, verbose=False):
        self.simulation_engine:SimulationEngine = simulation_engine
        self.initial_temp = initial_temp
        self.final_temp = final_temp
        self.alpha = alpha
        self.max_iter = max_iter
        self.nights_per_layout = nights_per_layout
        self.verbose = verbose

    def cost_function(self, layout_grid):
        total_tips = 0
        for _ in range(self.nights_per_layout):
            total_tips += self.simulation_engine.run(layout_grid)
        return -total_tips / self.nights_per_layout

    def _is_valid_table_pos(self, layout_grid, r, c):
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                
                nr, nc = r + dr, c + dc
                if 0 <= nr < len(layout_grid) and 0 <= nc < len(layout_grid[0]) and layout_grid[nr][nc] == PlaceType.TABLE:
                    return False
                
        return True
    
    def get_neighbor(self, layout_grid):
        new_grid = [row[:] for row in layout_grid]
        rows, cols = len(new_grid), len(new_grid[0])
        
        while True:
            x1, y1 = random.randint(0, rows - 1), random.randint(0, cols - 1)
            x2, y2 = random.randint(0, rows - 1), random.randint(0, cols - 1)
            
            if new_grid[x1][y1] == PlaceType.TABLE and new_grid[x2][y2] == PlaceType.FLOOR:
                new_grid[x1][y1], new_grid[x2][y2] = new_grid[x2][y2], new_grid[x1][y1]

                if self._is_valid_table_pos(layout_grid, x2, y2):
                    break
                
                new_grid[x1][y1], new_grid[x2][y2] = new_grid[x2][y2], new_grid[x1][y1]
                

        return new_grid
    
    
    def random_initial_config(self, layout_grid, num_tables):
        rows, cols = len(layout_grid), len(layout_grid[0])
        new_grid = [row[:] for row in layout_grid]  # Make a copy of the grid
        
        placed_tables = 0
        while placed_tables < num_tables:
            r, c = random.randint(0, rows - 1), random.randint(0, cols - 1)
            
            # Check if the spot is a floor and is not adjacent to another table
            if new_grid[r][c] == PlaceType.FLOOR and self._is_valid_table_pos(new_grid, r, c):
                new_grid[r][c] = PlaceType.TABLE
                placed_tables += 1
        
        return new_grid
    
    def simulated_annealing(self, initial_config):
        current_config = initial_config
        current_cost = self.cost_function(current_config)
        best_config = current_config
        best_cost = current_cost
        temp = self.initial_temp

        while temp > self.final_temp:
            for _ in range(self.max_iter):
                neighbor_config = self.get_neighbor(current_config)
                neighbor_cost = self.cost_function(neighbor_config)
                delta_cost = neighbor_cost - current_cost

                if delta_cost < 0 or random.uniform(0, 1) < math.exp(-delta_cost / temp):
                    current_config = neighbor_config
                    current_cost = neighbor_cost

                    if current_cost < best_cost:
                        best_config = current_config
                        best_cost = current_cost

            temp *= self.alpha

        return best_config, -best_cost
