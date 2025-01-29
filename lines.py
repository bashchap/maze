import csv

# Define the file name
filename = 'plot_data_2d.csv'

# Define the headers and data
headers = ['X', 'Y', 'Z']
data = [[64, 64, z] for z in range(1025)]

# Write to the CSV file
with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerows(data)

print(f"File {filename} created successfully.")