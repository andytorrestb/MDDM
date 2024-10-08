from src.input_utils import get_input, load_input_from_file, validate_input
from src.ballistics import calculate_initial_velocity, calculate_trajectory, calculate_launch_angle
from src.output_utils import plot_trajectory, save_trajectory_to_file

def main():
    # Step 1: Load or get input data
    try:
        data = load_input_from_file("data/input.json")
    except FileNotFoundError:
        data = get_input()
    
    validated_data = validate_input(data)
    
    # Step 2: Perform calculations
    v_0 = calculate_initial_velocity(
        validated_data['drag_coefficient'],
        validated_data['gas_density'],
        validated_data['particle_diameter'],
        validated_data['gas_velocity'],
        validated_data['gravity'],
        time_step=0.01
    )
    
    # Example plume characteristics
    plume_velocity = validated_data['gas_velocity']
    stagnation_velocity = 200  # Assumed vertical velocity at stagnation point (adjust as needed)
    radial_distance = 2  # Assumed distance from center of plume
    max_distance = 10  # Assumed maximum impingement zone
    
    launch_angle = calculate_launch_angle(plume_velocity, stagnation_velocity, radial_distance, max_distance)
    
    trajectory = calculate_trajectory(
        v_0,
        launch_angle,
        validated_data['gravity'],
        time_step=0.01,
        max_time=5
    )
    
    # Step 3: Output results
    plot_trajectory(trajectory)
    save_trajectory_to_file(trajectory, "results/trajectory.txt")

if __name__ == "__main__":
    main()
