import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class FuzzyTip:
    def __init__(self):
        # Define input variables
        self.waiting_time = ctrl.Antecedent(np.arange(0, 3601, 1), 'waiting_time')
        self.food_temp = ctrl.Antecedent(np.arange(25, 81, 1), 'food_temp')

        # Define output variable
        self.tip_percentage = ctrl.Consequent(np.arange(0, 26, 1), 'tip_percentage')

        # Define membership functions for waiting time
        self.waiting_time['short'] = fuzz.trapmf(self.waiting_time.universe, [0, 0, 300, 900])
        self.waiting_time['acceptable'] = fuzz.trimf(self.waiting_time.universe, [600, 1200, 2400])
        self.waiting_time['long'] = fuzz.trapmf(self.waiting_time.universe, [1800, 3000, 3600, 3600])

        # Define membership functions for food temperature
        self.food_temp['cold'] = fuzz.trapmf(self.food_temp.universe, [25, 25, 40, 50])
        self.food_temp['hot'] = fuzz.trapmf(self.food_temp.universe, [60, 70, 80, 80])

        # Define membership functions for tip percentage
        self.tip_percentage['low'] = fuzz.trimf(self.tip_percentage.universe, [0, 0, 8])
        self.tip_percentage['medium'] = fuzz.trimf(self.tip_percentage.universe, [5, 13, 21])
        self.tip_percentage['high'] = fuzz.trimf(self.tip_percentage.universe, [17, 25, 25])

        # Define fuzzy rules
        rule1 = ctrl.Rule(self.waiting_time['short'] & self.food_temp['hot'], self.tip_percentage['high'])
        rule2 = ctrl.Rule(self.waiting_time['acceptable'] | self.food_temp['cold'], self.tip_percentage['medium'])
        rule3 = ctrl.Rule(self.waiting_time['long'], self.tip_percentage['low'])
        self.rules = [rule1, rule2, rule3]

        # Create fuzzy control system
        self.tipping_ctrl = ctrl.ControlSystem(self.rules)

        # Create simulation object
        self.tipping = ctrl.ControlSystemSimulation(self.tipping_ctrl)

    def view(self):
        self.waiting_time.view()
        self.food_temp.view()
        self.tip_percentage.view()

    def get_tip(self, waiting_time, food_temp):
        # Input values
        self.tipping.input['waiting_time'] = waiting_time
        self.tipping.input['food_temp'] = food_temp

        # Compute output
        self.tipping.compute()

        # Return output
        return self.tipping.output['tip_percentage']