import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# Load the CSV file
file_path = "plot_data_4d.csv"  # Replace with the path to your CSV file
data = pd.read_csv(file_path)

# Ensure the columns are named X, Y, Z, and Frame
if not {'X', 'Y', 'Z', 'Frame'}.issubset(data.columns):
    raise ValueError("The CSV file must have 'X', 'Y', 'Z', and 'Frame' columns.")

# Filter out rows where Z < 0
data = data[data['Z'] >= 0]

# Get unique frame numbers
frames = sorted(data['Frame'].unique())

# Create a 3D scatter plot
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Initialize the scatter plot object
sc = ax.scatter([], [], [], c=[], cmap='viridis', marker='o')

# Add color bar
cbar = plt.colorbar(sc, ax=ax, shrink=0.5)
cbar.set_label('Z Value')

# Label the axes
ax.set_xlabel('X Coordinate')
ax.set_ylabel('Y Coordinate')
ax.set_zlabel('Z Coordinate')

# Set custom elevation and azimuth
ax.view_init(elev=90, azim=-90)

# Update function for animation
def update(frame):
    frame_data = data[data['Frame'] == frame]
    x = frame_data['X']
    y = frame_data['Y']
    z = frame_data['Z']

    print(f"> Frame: {frame}")
    # Update scatter plot
    sc._offsets3d = (x, y, z)
    sc.set_array(z)
    ax.set_title(f'3D Scatter Plot of Coordinates - Frame {frame}')
    return sc,

# Create the animation
anim = FuncAnimation(fig, update, frames=frames, interval=200, blit=False)

# Save the animation as a video file
output_file = "4D_anim.mpg"
anim.save(output_file, writer='ffmpeg', fps=5)

print(f"Animation saved as {output_file}")
