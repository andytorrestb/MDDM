import sys, os
# Add the src folder to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import unittest
import numpy as np
import matplotlib.pyplot as plt
from SALib.sample.morris import sample
from SALib.analyze.morris import analyze
from ballistics import calculate_trajectory_lane2012, calculate_initial_velocity

class TestMorrisSensitivity(unittest.TestCase):

    def setUp(self):
        """Set up the parameters for the Morris One-At-A-Time (MOAT) study."""
        # Define the problem with the input parameters and their ranges
        self.problem = {
            'num_vars': 4,  # We are varying 5 parameters
            'names': ['d_p', 'u_g', 'g', 'C_d'],
            'bounds': [
                [1e-6, 1e-4],       # Particle diameter in meters
                [100, 2000],        # Gas velocity in m/s
                [1.62, 9.8],        # Gravitational acceleration in m/s^2
                [0.1, 1]            # Drag coefficient
            ]
        }

    def model(self, params):
        """The model function to evaluate the trajectory based on the input parameters."""
        d_p = params[0]  # Particle diameter
        u_g = params[1]  # Gas velocity
        gravity = params[2]  # Gravity
        C_d = params[3]  # Drag coefficient

        # Constants for the Lane 2012 trajectory
        x_0 = 0.01  # Initial vertical position (assumed surface level)
        y_0 = 0.01  # Initial horizontal position (starting point)
        s_0 = 0.1  # Slope of the trajectory
        b = 0.05  # Curve-fitting parameter (adjust based on experimental data)
        v_0 = calculate_initial_velocity(C_d, 0.01, d_p, u_g, gravity, time_step=0.01)

        # Maximum horizontal distance for trajectory calculation
        max_distance = 100  # meters

        # Call Lane 2012 model to calculate the trajectory
        trajectory = calculate_trajectory_lane2012(x_0, y_0, s_0, b, gravity, v_0, max_distance)

        # Extract maximum horizontal distance and maximum height from the trajectory
        horizontal_distances, vertical_distances = zip(*trajectory)
        x_max = max(horizontal_distances)  # Maximum horizontal distance
        y_max = max(vertical_distances)    # Maximum vertical distance

        return x_max, y_max

    def test_morris(self):
        """Run the Morris sensitivity analysis and plot the results."""
        # Step 1: Generate the parameter samples using Morris sampling
        param_values = sample(self.problem, N=100, num_levels=4)

        # Step 2: Run the model for each parameter set and collect the outputs
        Y_x = np.array([self.model(params)[0] for params in param_values])  # x_max
        Y_y = np.array([self.model(params)[1] for params in param_values])  # y_max

        # Step 3: Perform the Morris analysis for x_max (horizontal distance)
        Si_x = analyze(self.problem, param_values, Y_x, num_resamples=100, conf_level=0.95, print_to_console=True, scaled = True)
        self.plot_sensitivity(Si_x, "Horizontal Distance (x_max)")

        # Step 4: Perform the Morris analysis for y_max (vertical distance)
        Si_y = analyze(self.problem, param_values, Y_y, num_resamples=100, conf_level=0.95, print_to_console=True, scaled = True)
        self.plot_sensitivity(Si_y, "Vertical Distance (y_max)")

    def plot_sensitivity(self, Si, title):
        """Plot the sensitivity indices from the Morris analysis."""
        plt.figure(figsize=(10, 6))
        plt.bar(self.problem['names'], Si['mu_star'])
        plt.title(f'Morris Sensitivity Analysis - {title}')
        plt.ylabel('Mean |mu*| (Sensitivity Index)')
        plt.grid(True)
        plt.savefig(f'moat-{title}.png')

if __name__ == '__main__':
    unittest.main()
