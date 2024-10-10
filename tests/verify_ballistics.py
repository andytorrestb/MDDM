import sys, os
# Add the src folder to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import unittest
import matplotlib.pyplot as plt
import pandas as pd
from ballistics import calculate_trajectory_lane2012

class TestLane2012Trajectory(unittest.TestCase):

    def test_lane2012_trajectory(self):
        """Test the Lane 2012 ballistics model and plot the trajectory."""
        # Define the input parameters based on Lane 2012
        g = 1.62        # Lunar gravity in m/s^2
        max_distance = 30 # Max horizontal distance in meters for the trajectory

        C1 = {'x_0':0.01, 'y_0':0.88779, 'D':1e-6, 'b':4.361, 's_0': 0.03662, 'v_0': 1983}
        C2 = {'x_0':0.01, 'y_0':2.4428, 'D':1e-6, 'b':11.09, 's_0': 0.03389, 'v_0': 528.7}  
        C3 = {'x_0':0.01, 'y_0':6.7215, 'D':1e-6, 'b':59.28, 's_0': 0.1089, 'v_0': 191}  
        curves = {'C1':C1, 'C2':C2, 'C3':C3}
        results = {}

        for curve in curves:
            # print(curves[curve])
            curve_data = curves[curve]
            x_0 = curve_data['x_0']
            y_0 = curve_data['y_0']
            s_0 = curve_data['s_0']
            b = curve_data['b']
            v_0 = curve_data['v_0']

            # Call the function to calculate the trajectory
            results[curve] = calculate_trajectory_lane2012(x_0, y_0, s_0, b, g, v_0, max_distance)
            # print(trajectory)
            # Plot the results

        self.plot_trajectory_compare(results)

    def plot_trajectory(self, trajectory, curve):
        """Plot the particle trajectory using matplotlib."""
        y_positions, x_positions = zip(*trajectory)

        lane_data = pd.read_csv(curve+'.csv')


        plt.figure(figsize=(10, 6))
        plt.plot(y_positions, x_positions, marker="o", linestyle="-", color="b", label = "Torres")
        plt.plot(lane_data['x'], lane_data[' y'], marker="o", linestyle=":", color="r", label = "Lane")
        plt.title("Particle Trajectory Based on Lane 2012 Model")
        plt.xlabel("Horizontal Distance (m)")
        plt.ylabel("Vertical Distance (m)")
        plt.legend()
        plt.yscale('log')
        plt.xscale('log')
        plt.grid(True)
        plt.savefig('trajectory_'+curve+'.png')
        plt.clf()

    def plot_trajectory_compare(self, results):
        """Plot the particle trajectory using matplotlib."""


        plt.figure(figsize=(10, 6))
        for curve in results:
            trajectory = results[curve]
            print(trajectory)
            y_positions, x_positions = zip(*trajectory)

            plt.plot(y_positions, x_positions, label = curve)

        plt.title("Particle Trajectory Based on Lane 2012 Model")
        plt.xlabel("Horizontal Distance (m)")
        plt.ylabel("Vertical Distance (m)")
        plt.legend()
        plt.yscale('log')
        plt.xscale('log')
        plt.grid(True)
        plt.savefig('trajectory_compare.png')
        plt.clf()

if __name__ == '__main__':
    unittest.main()
