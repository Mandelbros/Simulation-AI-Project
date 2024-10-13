import os, time
import json
import argparse
from src.SimulationEngine import SimulationEngine
from src.RestaurantOptimizer import RestaurantOptimizer 

# Configuración de argparse para la línea de comandos
parser = argparse.ArgumentParser(description='Restaurant Simulation')
parser.add_argument('--mode', type=str, choices=['optimizer', 'single_simulation'], default='single_simulation', help='Operation mode: optimizer or single_simulation')
parser.add_argument('--verbose', action='store_true', help='Enable verbose mode')
args = parser.parse_args()

# Obtener la ruta absoluta al directorio que contiene tu script
dir_path = os.path.dirname(os.path.realpath(__file__))

# Usar la ruta absoluta para abrir el archivo config.json
with open(os.path.join(dir_path, 'config.json')) as f:
    config = json.load(f)

# Crear una nueva instancia de SimulationEngine con la configuración cargada
simulation_engine = SimulationEngine(
    duration=config['simulation_duration'],
    arrival_rate=config['arrival_rate'],
    waiter_amount=config['number_of_waiters'],
    verbose=args.verbose
)

# Crear una instancia de SimulatedAnnealing
optimizer = RestaurantOptimizer(
    simulation_engine=simulation_engine,
    initial_temp=config['initial_temp'],
    final_temp=config['final_temp'],
    alpha=config['alpha'],
    max_iter=config['max_iter'],
    nights_per_layout=config['nights_per_layout'],
    initial_grid=config['optimizer_grid'],
    num_tables=config['number_of_tables'],
    verbose=args.verbose
)

start_time = time.time()

# Selección de modo de operación
if args.mode == 'optimizer':
    best_config, best_tips = optimizer.simulated_annealing()
    print("Mejor configuración:")
    for row in best_config:
        print(row)
    print("Mejores propinas promedio por noche:", best_tips)
elif args.mode == 'single_simulation':
    tips = simulation_engine.run(config['single_simulation_grid'])
    print("Propinas para una sola noche:", tips)

# End the timer and print the total execution time
end_time = time.time()
print("Total execution time: {} seconds".format(end_time - start_time))