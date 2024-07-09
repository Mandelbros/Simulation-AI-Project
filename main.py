import os,json
from src.SimulationEngine import SimulationEngine

# Get the absolute path to the directory containing your script
dir_path = os.path.dirname(os.path.realpath(__file__))

# Use the absolute path to open the config.json file
with open(os.path.join(dir_path, 'config.json')) as f:
    config = json.load(f)

# Crear una nueva instancia de SimulationEngine con la configuración cargada
simulation_engine = SimulationEngine(
    duration=config['simulation_duration'],
    lambda_rate=config['arrival_rate'],
    restaurant_grid=config['restaurant_grid'],
    table_amount=config['number_of_tables'],
    waiter_amount=config['number_of_waiters'],
    verbose=True
)

simulation_engine.run()
