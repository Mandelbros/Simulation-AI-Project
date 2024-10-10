import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import os
import pickle

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

class FuzzyTip:
    def __init__(self, precompute_file='lookup_table.pkl'):
        self.precompute_file = precompute_file

        # Definir variables de entrada
        self.waiting_time = ctrl.Antecedent(np.arange(0, 3601, 1), 'waiting_time')
        self.food_temp = ctrl.Antecedent(np.arange(25, 81, 1), 'food_temp')

        # Definir variable de salida
        self.tip_percentage = ctrl.Consequent(np.arange(0, 26, 1), 'tip_percentage')

        # Definir funciones de membresía para el tiempo de espera
        self.waiting_time['short'] = fuzz.trapmf(self.waiting_time.universe, [0, 0, 300, 900])
        self.waiting_time['acceptable'] = fuzz.trimf(self.waiting_time.universe, [600, 1200, 2400])
        self.waiting_time['long'] = fuzz.trapmf(self.waiting_time.universe, [1800, 3000, 3600, 3600])

        # Definir funciones de membresía para la temperatura de la comida
        self.food_temp['cold'] = fuzz.trapmf(self.food_temp.universe, [25, 25, 40, 50])
        self.food_temp['hot'] = fuzz.trapmf(self.food_temp.universe, [60, 70, 80, 80])

        # Definir funciones de membresía para el porcentaje de propina
        self.tip_percentage['low'] = fuzz.trimf(self.tip_percentage.universe, [0, 0, 8])
        self.tip_percentage['medium'] = fuzz.trimf(self.tip_percentage.universe, [5, 13, 21])
        self.tip_percentage['high'] = fuzz.trimf(self.tip_percentage.universe, [17, 25, 25])

        # Definir reglas difusas
        rule1 = ctrl.Rule(self.waiting_time['short'] & self.food_temp['hot'], self.tip_percentage['high'])
        rule2 = ctrl.Rule(self.waiting_time['acceptable'] | self.food_temp['cold'], self.tip_percentage['medium'])
        rule3 = ctrl.Rule(self.waiting_time['long'], self.tip_percentage['low'])
        rule4 = ctrl.Rule(~(self.waiting_time['short'] | self.waiting_time['acceptable'] | self.waiting_time['long']) |
                  ~(self.food_temp['cold'] | self.food_temp['hot']), self.tip_percentage['medium'])
        self.rules = [rule1, rule2, rule3, rule4]

        # Crear sistema de control difuso
        self.tipping_ctrl = ctrl.ControlSystem(self.rules)

        # Crear objeto de simulación
        self.tipping = ctrl.ControlSystemSimulation(self.tipping_ctrl)

        # Cargar o precomputar la tabla de búsqueda
        if os.path.exists(self.precompute_file):
            self.load_precomputed_values()
        else:
            self.lookup_table = {}
            self.precompute()
            self.save_precomputed_values()

    def precompute(self):
        # Iterar sobre todos los valores posibles de waiting_time y food_temp
        for waiting_time in range(0, 3601):
            for food_temp in range(25, 81):
                print(waiting_time,food_temp)
                try:
                    # Asignar entradas
                    self.tipping.input['waiting_time'] = waiting_time
                    self.tipping.input['food_temp'] = food_temp

                    # Calcular la salida
                    self.tipping.compute()

                    # Guardar el resultado en la tabla de búsqueda
                    self.lookup_table[(waiting_time, food_temp)] = self.tipping.output['tip_percentage']
                except ValueError:
                    # Asignar valor por defecto si ocurre un error
                    self.lookup_table[(waiting_time, food_temp)] = 0

    def save_precomputed_values(self):
        # Guardar la tabla de búsqueda en un archivo utilizando pickle
        with open(self.precompute_file, 'wb') as f:
            pickle.dump(self.lookup_table, f)

    def load_precomputed_values(self):
        # Cargar la tabla de búsqueda desde un archivo utilizando pickle
        with open(self.precompute_file, 'rb') as f:
            self.lookup_table = pickle.load(f)

    def get_tip(self, waiting_time, food_temp):
        # Recuperar el valor precalculado de la tabla de búsqueda
        return self.lookup_table[(waiting_time, food_temp)]
    
    def plot_3d(self):
        # Crear listas para los valores de waiting_time, food_temp y tip_percentage
        waiting_times = []
        food_temps = []
        tip_percentages = []

        for (waiting_time, food_temp), tip_percentage in self.lookup_table.items():
            waiting_times.append(waiting_time)
            food_temps.append(food_temp)
            tip_percentages.append(tip_percentage)

        # Convertir las listas a arrays de numpy para graficar
        waiting_times = np.array(waiting_times)
        food_temps = np.array(food_temps)
        tip_percentages = np.array(tip_percentages)

        # Crear la figura y los ejes 3D
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Crear la gráfica de dispersión 3D
        scatter = ax.scatter(waiting_times, food_temps, tip_percentages, c=tip_percentages, cmap='viridis')

        # Etiquetas de los ejes
        ax.set_xlabel('Waiting Time (s)')
        ax.set_ylabel('Food Temperature (°C)')
        ax.set_zlabel('Tip Percentage (%)')

        # Añadir barra de colores para indicar el valor de la propina
        fig.colorbar(scatter, ax=ax, label='Tip Percentage (%)')

        # Mostrar la gráfica
        plt.show()

# Ejemplo de uso
#fuzzy_tip = FuzzyTip()
#fuzzy_tip.plot_3d()
