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

def calculate_trajectory(v_0, launch_angle, gravity, initial_position=(0, 1), time_step=0.01, max_time=20e5):
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
