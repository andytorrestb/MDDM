import sys, os
# Add the src folder to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import unittest
import matplotlib.pyplot as plt
from ballistics import calculate_trajectory_lane2012

class TestLane2012Trajectory(unittest.TestCase):

    def test_lane2012_trajectory(self):
        """Test the Lane 2012 ballistics model and plot the trajectory."""
        # Define the input parameters based on Lane 2012
        x_0 = 1         # Initial vertical position (surface level)
        y_0 = 0.1         # Initial horizontal position (assumed to start at 0)
        s_0 = 0.1       # Initial slope of the trajectory (based on plume forces)
        b = 0.05        # Curve-fitting parameter to match plume behavior
        g = 1.62        # Lunar gravity in m/s^2
        v_0 = 500       # Initial horizontal velocity in m/s
        max_distance = 100  # Max horizontal distance in meters for the trajectory

        # Call the function to calculate the trajectory
        trajectory = calculate_trajectory_lane2012(x_0, y_0, s_0, b, g, v_0, max_distance)
        print(trajectory)
        # Plot the results
        self.plot_trajectory(trajectory)

    def plot_trajectory(self, trajectory):
        """Plot the particle trajectory using matplotlib."""
        y_positions, x_positions = zip(*trajectory)

        plt.figure(figsize=(10, 6))
        plt.plot(y_positions, x_positions, marker="o", linestyle="-", color="b")
        plt.title("Particle Trajectory Based on Lane 2012 Model")
        plt.xlabel("Horizontal Distance (m)")
        plt.ylabel("Vertical Distance (m)")
        plt.grid(True)
        plt.savefig('trajectory.png')
        plt.clf()

if __name__ == '__main__':
    unittest.main()
