import numpy as np
from stl import mesh

def stl_to_xyz_vectors(stl_file):
    # Load the STL file
    stl_mesh = mesh.Mesh.from_file(stl_file)
    
    # Extract the vectors (triangles)
    vectors = stl_mesh.vectors  # Shape (N, 3, 3), where N is the number of triangles
    
    # Reshape into rows of x, y, z coordinates
    xyz_rows = vectors.reshape(-1, 3)  # Flatten into individual XYZ points
    
    return xyz_rows

# Example usage
stl_file = "example.stl"  # Replace with your STL file path
xyz_data = stl_to_xyz_vectors(stl_file)

# Save to CSV file if needed
np.savetxt("output.csv", xyz_data, delimiter=",", header="X,Y,Z", comments='')

# Display first few rows
print(xyz_data[:5])  # Print first 5 rows of XYZ data