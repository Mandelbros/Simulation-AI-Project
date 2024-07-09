import json
from src.SimulationEngine import SimulationEngine

# Cargar la configuración del archivo JSON
with open('config.json') as f:
    config = json.load(f)

# Crear una nueva instancia de SimulationEngine con la configuración cargada
simulation_engine = SimulationEngine(
    duration=config['simulation_duration'],
    restaurant_grid=config['restaurant_grid'],
    table_amount=config['number_of_tables'],
    waiter_amount=config['number_of_waiters']
)
