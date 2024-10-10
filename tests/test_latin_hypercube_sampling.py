import sys
import os
import unittest
import numpy as np
import matplotlib.pyplot as plt
from pyDOE import lhs  # Latin Hypercube Sampling

# Add the src folder to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Import the necessary functions from the ballistics module
from ballistics import calculate_trajectory_lane2012, calculate_initial_velocity

class TestLatinHypercubeSampling(unittest.TestCase):

    def test_lhs_varying_diameter_and_gravity(self):
        """Test and plot particle trajectories for Latin Hypercube Sampling (LHS) over particle diameter and gravity."""
        
        # Define constants for the Lane 2012 trajectory model
        x_0 = 0.01        # Initial vertical position (above surface)
        y_0 = 0.01        # Initial horizontal position (slightly off center)
        s_0 = 0.1         # Initial slope of the trajectory
        b = 0.05          # Curve-fitting parameter for trajectory curvature
        gas_velocity = 1000  # Assumed gas velocity in m/s
        drag_coefficient = 0.5  # Drag coefficient for the particles
        max_distance = 100  # Maximum horizontal distance for calculation in meters

        # Define ranges for particle diameter and gravity
        d_p_range = [1e-6, 50e-6]  # Particle diameters from 1 micron to 50 microns
        g_range = [1.62, 9.8]      # Gravity from lunar (1.62 m/s^2) to Earth gravity (9.8 m/s^2)

        # Number of samples for Latin Hypercube Sampling
        num_samples = 5

        # Generate Latin Hypercube Samples for particle diameter and gravity
        lhs_samples = lhs(2, samples=num_samples)  # LHS for 2 variables
        particle_diameters = d_p_range[0] + (d_p_range[1] - d_p_range[0]) * lhs_samples[:, 0]  # Scaled to d_p range
        gravities = g_range[0] + (g_range[1] - g_range[0]) * lhs_samples[:, 1]  # Scaled to gravity range

        # Plot colors for the trajectories
        colors = ['r', 'g', 'b', 'm', 'c']

        # Initialize the plot
        plt.figure(figsize=(10, 6))

        # Loop through each LHS sample, calculate the trajectory, and plot it
        for i in range(num_samples):
            d_p = particle_diameters[i]
            gravity = gravities[i]

            # Calculate the initial velocity for the given particle diameter and gravity
            v_0 = calculate_initial_velocity(drag_coefficient, 0.01, d_p, gas_velocity, gravity, time_step=0.01)

            # Calculate the trajectory using the Lane 2012 model
            trajectory = calculate_trajectory_lane2012(x_0, y_0, s_0, b, gravity, v_0, max_distance)

            # Extract the x (horizontal) and y (vertical) positions
            y_positions, x_positions = zip(*trajectory)

            # Plot the trajectory with a label indicating the particle diameter and gravity
            plt.plot(y_positions, x_positions, color=colors[i], label=f'd_p = {d_p:.1e} m, g = {gravity:.2f} m/s^2')

        # Add labels, title, and legend to the plot
        plt.title('Particle Trajectories with Latin Hypercube Sampling (LHS)')
        plt.xlabel('Horizontal Distance (m)')
        plt.ylabel('Vertical Distance (m)')
        plt.grid(True)
        plt.legend()
        
        plt.savefig('latin_hypercube.png')
        # Display the plot
        plt.show()

if __name__ == '__main__':
    unittest.main()
