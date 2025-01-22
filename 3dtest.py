import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# Generate random 3D data
np.random.seed(0)
x = np.random.rand(100) * 10
y = np.random.rand(100) * 10
z = np.random.rand(100) * 10

# Create the figure and 3D axes
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Scatter plot
sc = ax.scatter(x, y, z, c=z, cmap='viridis', marker='o')

# Function to update the rotation angle
def update(frame):
    ax.view_init(elev=20, azim=frame)
    return sc,

# Create the animation
ani = FuncAnimation(fig, update, frames=range(0, 360, 2), interval=50, blit=False)

# Show the animation
plt.show()
