def estimate_gas_velocity(thrust, nozzle_area, altitude, exhaust_velocity):
    """Estimate the gas velocity at the surface based on thrust and nozzle parameters."""
    pressure_ratio = 101325 / (101325 + thrust / nozzle_area)
    u_g = exhaust_velocity * (1 - pressure_ratio**0.5)
    return u_g

def estimate_drag_coefficient(particle_diameter):
    """Return a drag coefficient based on particle properties."""
    # You can use empirical data or a look-up table
    return 0.5  # Approximation for spherical particles
