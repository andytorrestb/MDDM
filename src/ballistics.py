import math

def calculate_drag_force(C_d, rho_g, A_p, u_g, v_0):
    """Calculate the drag force on the particle."""
    return 0.5 * C_d * rho_g * A_p * (u_g - v_0)**2

def calculate_initial_velocity(C_d, rho_g, d_p, u_g, gravity, time_step):
    """Estimate the initial velocity of the particle."""
    A_p = math.pi * (d_p / 2)**2
    m_p = (4/3) * math.pi * (d_p / 2)**3 * 3000  # Assuming lunar regolith density ~3000 kg/m^3
    
    drag_force = calculate_drag_force(C_d, rho_g, A_p, u_g, 0)
    acceleration = (drag_force - m_p * gravity) / m_p
    v_0 = acceleration * time_step
    
    return v_0

def calculate_trajectory_lane2012(x_0, y_0, s_0, b, g, v_0, max_distance):
    """
    Calculate the trajectory of a particle based on the ballistics model presented in Lane 2012.

    :param x_0: Initial vertical position (usually 0 for surface launch).
    :param y_0: Initial horizontal position (initial distance from plume center).
    :param s_0: Derivative of trajectory at the starting point (slope of the trajectory).
    :param b: Curve-fitting parameter affecting the trajectory curvature.
    :param g: Gravitational acceleration (1.62 m/s^2 for the Moon).
    :param v_0: Horizontal velocity (assumed constant).
    :param max_distance: Maximum horizontal distance to compute (m).
    :return: List of (x, y) coordinates representing the trajectory.
    """
    trajectory = []
    y = y_0
    x = x_0
    step_size = 0.1
    while x >= 0:
        # Avoid division by zero when y == y_0
        if abs(y - y_0) < 1e-6:
            y += step_size
            continue

        # Calculate vertical position using Lane 2012's formula
        x = (x_0 + s_0 * (y - y_0)) + (b * (x_0 - s_0 * y_0) / (y - y_0)) - (g * (y - y_0)**2) / (2 * v_0**2)
        
        # Stop if the particle reaches the surface
        if x < 0:
            break
        
        trajectory.append((y, x))
        y += 0.1  # Increment horizontal position by 0.1 m (or a finer resolution as needed)
    
    return trajectory

def calculate_launch_angle(plume_velocity, stagnation_velocity, radial_distance, max_distance):
    """
    Calculate the initial launch angle of particles based on the plume velocity and surface characteristics.
    
    :param plume_velocity: Gas velocity near the surface in m/s.
    :param stagnation_velocity: Vertical gas velocity at the stagnation point (center of plume) in m/s.
    :param radial_distance: Distance from the center of the plume in meters.
    :param max_distance: Maximum radius of the impingement zone in meters.
    :return: Launch angle in degrees.
    """
    # Estimate the radial velocity (horizontal component) at distance r
    v_x = plume_velocity * (radial_distance / max_distance)
    
    # Estimate the vertical velocity (vertical component) at distance r
    v_y = stagnation_velocity * (1 - radial_distance / max_distance)
    
    # Calculate the launch angle (in radians)
    theta = math.atan2(v_y, v_x)
    
    # Convert to degrees
    theta_deg = math.degrees(theta)
    
    return theta_deg

def calculate_trajectory(v_0, launch_angle, gravity, initial_position=(0, 0), time_step=0.01, max_time=10):
    """Compute the particle trajectory based on initial velocity, angle, and gravity."""
    x_0, y_0 = initial_position
    theta = math.radians(launch_angle)  # Convert angle to radians

    # Decompose initial velocity into horizontal and vertical components
    v_0x = v_0 * math.cos(theta)
    v_0y = v_0 * math.sin(theta)

    trajectory = [(x_0, y_0)]
    t = 0

    while t <= max_time:
        # Calculate position at time t
        x = x_0 + v_0x * t
        y = y_0 + v_0y * t - 0.5 * gravity * t**2

        # Stop if the particle hits the ground
        if y <= 0:
            break

        trajectory.append((x, y))
        t += time_step

    return trajectory
