import sys
import os
import unittest
import matplotlib.pyplot as plt

# Add the src folder to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from ballistics import calculate_initial_velocity, calculate_trajectory, calculate_launch_angle

class TestBallistics(unittest.TestCase):

    def test_initial_velocity(self):
        """Test the calculation of initial velocity with varying particle diameter."""
        C_d = 0.5  # drag coefficient
        rho_g = 0.01  # gas density in kg/m^3 (assumed)
        u_g = 500  # gas velocity in m/s
        gravity = 1.62  # lunar gravity in m/s^2
        time_step = 0.01  # time step for velocity calculation

        # Test different particle diameters and store initial velocities
        particle_diameters = [1e-6, 5e-6, 10e-6, 20e-6, 50e-6]  # diameters in meters
        initial_velocities = []

        for d_p in particle_diameters:
            v_0 = calculate_initial_velocity(C_d, rho_g, d_p, u_g, gravity, time_step)
            initial_velocities.append(v_0)

        # Plot initial velocities as a function of particle diameter
        self.plot_initial_velocity(particle_diameters, initial_velocities)

    def test_trajectory(self):
        """Test the calculation of the particle trajectory with varying launch angles."""
        v_0 = 50  # initial velocity in m/s
        gravity = 1.62  # lunar gravity in m/s^2
        time_step = 0.01  # time step in seconds
        max_time = 5000  # run for 5 seconds

        launch_angles = [15, 30, 45, 60, 75]  # Launch angles in degrees
        trajectories = []

        for launch_angle in launch_angles:
            trajectory = calculate_trajectory(v_0, launch_angle, gravity, time_step=time_step, max_time=max_time)
            trajectories.append(trajectory)

        # Plot trajectories for different launch angles
        self.plot_trajectory(trajectories, launch_angles)

    def test_launch_angle(self):
        """Test the launch angle calculation with varying radial distances."""
        plume_velocity = 500  # m/s (horizontal gas velocity near the surface)
        stagnation_velocity = 200  # m/s (vertical gas velocity at stagnation point)
        max_distance = 10  # meters (maximum impingement zone radius)
        radial_distances = [1, 3, 5, 7, 9]  # distances from plume center

        launch_angles = []

        for radial_distance in radial_distances:
            angle = calculate_launch_angle(plume_velocity, stagnation_velocity, radial_distance, max_distance)
            launch_angles.append(angle)

        # Plot launch angle as a function of radial distance
        self.plot_launch_angle(radial_distances, launch_angles)

    def plot_initial_velocity(self, particle_diameters, initial_velocities):
        """Plot the initial velocity as a function of particle diameter."""
        plt.figure(figsize=(8, 5))
        plt.plot(particle_diameters, initial_velocities, marker="o", linestyle="-", color="r")
        plt.title("Initial Velocity vs Particle Diameter")
        plt.xlabel("Particle Diameter (m)")
        plt.ylabel("Initial Velocity (m/s)")
        plt.grid(True)
        plt.xscale('log')  # Use logarithmic scale for particle diameters
        plt.savefig('initial_velocity.png')
        plt.clf()   

    def plot_trajectory(self, trajectories, launch_angles):
        """Plot particle trajectories for different launch angles."""
        plt.figure(figsize=(8, 5))
        for trajectory, angle in zip(trajectories, launch_angles):
            x, y = zip(*trajectory)
            plt.plot(x, y, label=f"Launch Angle: {angle}°")

        plt.title("Particle Trajectories for Different Launch Angles")
        plt.xlabel("Horizontal Distance (m)")
        plt.ylabel("Vertical Distance (m)")
        plt.legend()
        plt.grid(True)
        plt.savefig('trajectory.png')
        plt.clf()   

    def plot_launch_angle(self, radial_distances, launch_angles):
        """Plot launch angle as a function of radial distance."""
        plt.figure(figsize=(8, 5))
        plt.plot(radial_distances, launch_angles, marker="o", linestyle="-", color="b")
        plt.title("Launch Angle vs Radial Distance")
        plt.xlabel("Radial Distance (m)")
        plt.ylabel("Launch Angle (degrees)")
        plt.grid(True)
        plt.savefig('launch_angles.png')
        plt.clf()   

if __name__ == '__main__':
    unittest.main()
