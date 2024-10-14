import streamlit as st 
from src.GeminiClient import GeminiClient
import json
from src.SimulationEngine import SimulationEngine
from src.RestaurantOptimizer import RestaurantOptimizer 
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(dir_path, 'config.json')) as f:
    config = json.load(f)

# Function to display the main page with buttons
def main_page():
    st.title("Welcome")
   
    if st.button('Restaurant Optimizer'):
        st.session_state.page = 'optimizer'
        st.rerun()
    if st.button('Single Simulation'):
        st.session_state.page = 'simulator'
        st.rerun()

# Function to display the optimizer page
def optimizer_page():
    st.title("Restaurant Optimizer")
    
    # Text area for user input
    natural_language_config = st.text_area(
        "Introduzca en lenguaje natural la configuración para el optimizer:", 
        placeholder="Escriba la configuración aquí..."
    )

    # Button to trigger the LLM call
    if st.button('Update Configuration'):
        if natural_language_config.strip() != "":
            # Use spinner while the request is processed
            with st.spinner('Enviando configuración a Gemini...'): 
                # Llamada al cliente Gemini con la configuración proporcionada
                client = GeminiClient()
                response = client.send_to_gemini(natural_language_config)
                client.process_gemini_response(response)

            # Mostrar el resultado (puedes modificar esto según lo que devuelva tu API)
            st.success("¡Configuración enviada con éxito!")

    # Botón para comenzar la simulación usando el optimizador
    if st.button('Run Optimizer'):  
        simulation_engine = SimulationEngine(
            duration=config['simulation_duration'],
            arrival_rate=config['arrival_rate'],
            waiter_amount=config['number_of_waiters'],
            # verbose=args.verbose
        )

        optimizer = RestaurantOptimizer(
            simulation_engine=simulation_engine,
            initial_temp=config['initial_temp'],
            final_temp=config['final_temp'],
            alpha=config['alpha'],
            max_iter=config['max_iter'],
            nights_per_layout=config['nights_per_layout'],
            initial_grid=config['optimizer_grid'],
            num_tables=config['number_of_tables'],
            rules_priority=config['rules_priority'],
            # verbose=args.verbose
        )

        # Ejecuta el proceso de simulated annealing
        with st.spinner('Ejecutando simulación...'):
            best_config, best_tips = optimizer.simulated_annealing()

        # Mostrar los resultados de la simulación
        st.success("Simulación completada con éxito!")
        st.write(f"Mejor configuración: {best_config}")
        st.write(f"Mejor promedio de propinas por noche: {best_tips}")

    if st.button('Back'):
        st.session_state.page = 'main'
        st.rerun()

# Function to display the cows page
def simulator_page():
    st.title("Single Simulation")
    # st.write("Here is some information about cows.")

    if st.button('Run Single Simulation'):  
        simulation_engine = SimulationEngine(
            duration=config['simulation_duration'],
            arrival_rate=config['arrival_rate'],
            waiter_amount=config['number_of_waiters'],
            # verbose=args.verbose
        )

        total_tips = 0
        nights_per_layout = config['nights_per_layout']

        with st.spinner('Ejecutando simulación...'):
            for _ in range(nights_per_layout):
                simulation_tips = simulation_engine.run(config['single_simulation_grid'], config['rules_priority'])
                total_tips += simulation_tips
        
        st.success("Simulación completada con éxito!")
        st.write(f"Promedio de propinas: ", total_tips / nights_per_layout) 

    if st.button('Back'):
        st.session_state.page = 'main'
        st.rerun()

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'main'

# Navigation logic
if st.session_state.page == 'main':
    main_page()
elif st.session_state.page == 'optimizer':
    optimizer_page()
elif st.session_state.page == 'simulator':
    simulator_page()