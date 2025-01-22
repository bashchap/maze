import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# Load the CSV file
file_path = "your_file.txt"  # Replace with the path to your CSV file
data = pd.read_csv(file_path)

# Ensure the columns are named X, Y, Z
if not {'X', 'Y', 'Z'}.issubset(data.columns):
    raise ValueError("The CSV file must have 'X', 'Y', 'Z' columns.")

# Extract coordinates
x = data['X']
y = data['Y']
z = data['Z']

# Create the figure and 3D axes
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Scatter plot
sc = ax.scatter(x, y, z, c=z, cmap='viridis', marker='o')

# Add a color bar
cbar = plt.colorbar(sc, ax=ax, shrink=0.5)
cbar.set_label('Z Value')

# Label the axes
ax.set_xlabel('X Coordinate')
ax.set_ylabel('Y Coordinate')
ax.set_zlabel('Z Coordinate')

# Set the initial view angle
ax.view_init(elev=20, azim=30)

# Function to update the rotation angle
def update(frame):
    ax.view_init(elev=20, azim=frame)
    return sc,

# Create the animation
ani = FuncAnimation(fig, update, frames=range(0, 360, 2), interval=50, blit=False)

# Save animation as GIF (optional)
ani.save("3d_scatter_rotation.gif", writer="pillow")

# Show the animation
plt.show()
