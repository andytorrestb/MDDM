import sys
import os
import unittest
import matplotlib.pyplot as plt

# Add the src folder to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Import the necessary functions from the ballistics module
from ballistics import calculate_trajectory_lane2012, calculate_initial_velocity

class TestTrajectoryVaryingParticleDiameter(unittest.TestCase):

    def test_trajectory_for_varying_particle_diameter(self):
        """Test and save particle trajectories for varying particle diameter values."""
        
        # Define constants for the Lane 2012 trajectory model
        x_0 = 0.01       # Initial vertical position (above surface)
        y_0 = 0.01       # Initial horizontal position (slightly off center)
        s_0 = 0.1        # Initial slope of the trajectory
        b = 0.05         # Curve-fitting parameter for trajectory curvature
        gravity = 1.62   # Lunar gravity in m/s^2
        gas_velocity = 1000  # Assumed gas velocity in m/s
        drag_coefficient = 0.5  # Drag coefficient for the particles
        max_distance = 100  # Maximum horizontal distance for calculation in meters

        # Range of particle diameters (in meters)
        particle_diameters = [1e-6, 5e-6, 10e-6, 20e-6, 50e-6]  # Particle diameters from 1 micron to 50 microns

        # Plot colors for the trajectories
        colors = ['r', 'g', 'b', 'm', 'c']

        # Initialize the plot
        plt.figure(figsize=(10, 6))

        # Loop through each particle diameter, calculate the trajectory, and plot it
        for i, d_p in enumerate(particle_diameters):
            # Calculate the initial velocity for the given particle diameter
            v_0 = calculate_initial_velocity(drag_coefficient, 0.01, d_p, gas_velocity, gravity, time_step=0.01)

            # Calculate the trajectory using the Lane 2012 model
            trajectory = calculate_trajectory_lane2012(x_0, y_0, s_0, b, gravity, v_0, max_distance)

            # Extract the x (horizontal) and y (vertical) positions
            y_positions, x_positions = zip(*trajectory)

            # Plot the trajectory with a label indicating the particle diameter
            plt.plot(y_positions, x_positions, color=colors[i], label=f'd_p = {d_p:.1e} m')

        # Add labels, title, and legend to the plot
        plt.title('Particle Trajectories for Varying Particle Diameter Values')
        plt.xlabel('Horizontal Distance (m)')
        plt.ylabel('Vertical Distance (m)')
        plt.grid(True)
        plt.legend()

        # Save the plot to a file
        output_dir = "results"
        os.makedirs(output_dir, exist_ok=True)  # Ensure the output directory exists
        output_file = os.path.join(output_dir, 'particle_trajectories_varying_particle_diameter.png')
        plt.savefig(output_file)

        # Close the plot after saving
        plt.close()

        print(f"Graph saved to {output_file}")

if __name__ == '__main__':
    unittest.main()
