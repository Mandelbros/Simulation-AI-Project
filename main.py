import json
from classes.SimulationEngine import SimulationEngine

# Cargar la configuración del archivo JSON
with open('config.json') as f:
    config = json.load(f)

# Crear una nueva instancia de SimulationEngine con la configuración cargada
simulation_engine = SimulationEngine(config['restaurant_grid'])
