import matplotlib.pyplot as plt

def save_trajectory_to_file(trajectory, file_path):
    """Save trajectory data to a file."""
    with open(file_path, 'w') as f:
        for point in trajectory:
            f.write(f"{point[0]}, {point[1]}\n")

def plot_trajectory(trajectory):
    """Plot the particle trajectory."""
    x, y = zip(*trajectory)
    plt.figure(figsize=(8, 5))
    plt.plot(x, y, marker="o", linestyle="-", color="b")
    plt.title("Particle Trajectory")
    plt.xlabel("Horizontal Distance (m)")
    plt.ylabel("Vertical Distance (m)")
    plt.grid(True)
    plt.show()
