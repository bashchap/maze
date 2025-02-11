import csv

# Initialize the list to hold the coordinate tuples
xy_plane = []

# Read the CSV file
with open("duff.csv", mode="r") as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    for row in reader:
        xy_plane.append((float(row[0]), float(row[1]), float(row[2])))

# Print to verify
print(xy_plane)

