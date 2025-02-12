import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Load the CSV file
file_path = "plot_data_3d.csv"  # Replace with the path to your CSV file
data = pd.read_csv(file_path)

# Ensure the columns are named X, Y, Z
if not {'X', 'Y', 'Z'}.issubset(data.columns):
    raise ValueError("The CSV file must have 'X', 'Y', 'Z' columns.")

# Filter out rows where Z < 0
#data = data[data['Z'] >= 0]

# Extract coordinates
x = data['X']
y = data['Y']
z = data['Z']

# Create a 3D scatter plot
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Plot the points
sc = ax.scatter(x, y, z, c=z, cmap='viridis', marker='o')

# Add color bar
cbar = plt.colorbar(sc, ax=ax, shrink=0.5)
cbar.set_label('Z Value')

# Label the axes
ax.set_xlabel('X Coordinate')
ax.set_ylabel('Y Coordinate')
ax.set_zlabel('Z Coordinate')



ax.set_aspect('equal', adjustable='box')
# Adjust layout to remove padding
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
# Set full-screen mode
#manager = plt.get_current_fig_manager()
#manager.full_screen_toggle()



# Add a title
ax.set_title('3D Scatter Plot of Coordinates')

# Set custom elevation and azimuth
ax.view_init(elev=90, azim=-90)

# Show the plot
plt.show()
