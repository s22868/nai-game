"""

Authors: Mateusz Budzyński, Igor Gutowski

==========================================
Fuzzy Control Systems: Calculate Average Fuel Consumption
==========================================
To run program install
pip install scikit-fuzzy
pip install matplotlib


The following example concerns the calculation of average fuel consumption
based on the weight of the car, average speed and power.

We would formulate this problem as:

* Antecednets (Inputs)
   - `car weight`
      * Universe (ie, crisp value range): How heavy is the car, on a scale of 1000 to 3000 kg?
      * Fuzzy set (ie, fuzzy value range): light, medium, heavy
   - `average speed`
      * Universe: How fast is the car going, on a scale of 40 to 200 km/h?
      * Fuzzy set: slow, medium, fast
   - `power`
        * Universe: How powerful is the car, on a scale of 100 to 300 hp?
        * Fuzzy set: low, medium, high

* Consequents (Outputs)
   - `average fuel consumption`
      * Universe: How much fuel does the car consume, on a scale of 4 to 16 l/100km?
      * Fuzzy set: low, average, high
* Rules
   - IF the car is light AND the average speed is slow AND the power is low, THEN the average fuel consumption is low.
   - IF the car is medium AND the average speed is medium AND the power is medium, THEN the average fuel consumption is average.
   - IF the car is heavy AND the average speed is fast AND the power is high, THEN the average fuel consumption is high.
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

def calculate_average_fuel_consumption(car_weight_value, average_speed_value, power_value):
    """
    Function calculates average fuel consumption based on given vehicle parameters.
    
    :param car_weight_value: Car weight (kg)
    :param average_speed_value: Average speed (km/h)
    :param power_value: Vehicle power (horsepower)
    :return: Calculated average fuel consumption (l/100km)
    """

    """
    New Antecedent/Consequent objects hold universe variables and membership
    functions
    """
    car_weight = ctrl.Antecedent(np.arange(1000, 3000, 500), 'car_weight')
    average_speed = ctrl.Antecedent(np.arange(40, 200, 15), 'average_speed')
    power = ctrl.Antecedent(np.arange(100, 300, 10), 'power')
    average_fuel_consumption = ctrl.Consequent(np.arange(4, 16, 1), 'average_fuel_consumption')

    # Auto-membership function population is possible with .automf(3, 5, or 7)
    car_weight.automf(3, names=['light', 'medium', 'heavy'])
    average_speed.automf(3, names=['slow', 'medium', 'fast'])
    power.automf(3, names=['low', 'medium', 'high'])
    """
    Custom membership functions can be built interactively with a familiar,
    Pythonic API
    """
    average_fuel_consumption['low'] = fuzz.trimf(average_fuel_consumption.universe, [4, 4, 6])
    average_fuel_consumption['average'] = fuzz.trimf(average_fuel_consumption.universe, [6, 7, 10])
    average_fuel_consumption['high'] = fuzz.trimf(average_fuel_consumption.universe, [10, 15, 15])
    """
    Fuzzy rules
    -----------

    Now, to make these triangles useful, we define the *fuzzy relationship*
    between input and output variables. For the purposes of our example, consider
    three simple rules:

   - IF the car is light AND the average speed is slow AND the power is low, THEN the average fuel consumption is low.
   - IF the car is medium AND the average speed is medium AND the power is medium, THEN the average fuel consumption is average.
   - IF the car is heavy AND the average speed is fast AND the power is high, THEN the average fuel consumption is high.
    """
    rule1 = ctrl.Rule(car_weight['light'] & average_speed['slow'] & power['low'], average_fuel_consumption['low'])
    rule2 = ctrl.Rule(car_weight['medium'] & average_speed['medium'] & power['medium'], average_fuel_consumption['average'])
    rule3 = ctrl.Rule(car_weight['heavy'] & average_speed['fast'] & power['high'], average_fuel_consumption['high'])
    """
    Now that we have our rules defined, we can simply create a control system
    """
    average_fuel_consumption_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])

    """
    In order to simulate this control system, we will create a
    ``ControlSystemSimulation``.  Think of this object representing our controller
    applied to a specific set of cirucmstances.
    """
    fuel_sim = ctrl.ControlSystemSimulation(average_fuel_consumption_ctrl)

    """
    We can now simulate our control system by simply specifying the inputs
    and calling the ``compute`` method.
    """
    fuel_sim.input['car_weight'] = car_weight_value
    fuel_sim.input['average_speed'] = average_speed_value
    fuel_sim.input['power'] = power_value

    fuel_sim.compute()

    """
    Once computed, we can view the result as well as visualize it.
    """
    car_weight.view(sim=fuel_sim)
    average_speed.view(sim=fuel_sim)
    power.view(sim=fuel_sim)
    average_fuel_consumption.view(sim=fuel_sim)

    # Return average fuel consumption
    return fuel_sim.output['average_fuel_consumption']

# Example input data
car_weight_input = 1800
average_speed_input = 100
power_input = 150

# Calculate average fuel consumption
result = calculate_average_fuel_consumption(car_weight_input, average_speed_input, power_input)
print(f"Średnie spalanie paliwa: {result:.2f}")

plt.show()  # Shows plot
