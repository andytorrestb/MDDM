import json

def load_input_from_file(file_path):
    """Load input parameters from a JSON file."""
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def validate_input(data):
    """Validate input to ensure necessary parameters are provided and correct."""
    required_fields = ['gas_velocity', 'particle_diameter', 'drag_coefficient', 'gas_density', 'gravity']
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required input: {field}")
    return data

def get_input():
    """Prompt user for inputs if needed."""
    gas_velocity = float(input("Enter gas velocity (m/s): "))
    particle_diameter = float(input("Enter particle diameter (m): "))
    drag_coefficient = float(input("Enter drag coefficient: "))
    gas_density = float(input("Enter gas density (kg/m^3): "))
    gravity = float(input("Enter gravitational acceleration (m/s^2): "))
    
    return {
        'gas_velocity': gas_velocity,
        'particle_diameter': particle_diameter,
        'drag_coefficient': drag_coefficient,
        'gas_density': gas_density,
        'gravity': gravity
    }
