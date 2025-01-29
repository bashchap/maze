import curses
import pandas as pd

# Load the CSV file
file_path = "plot_data_2d.csv"
df = pd.read_csv(file_path)

# Extract X and Y coordinates
x_values = df['X'].tolist()
y_values = df['Y'].tolist()

def normalize(value, min_val, max_val, target_min, target_max):
    """Normalize values to fit within target range."""
    return int((value - min_val) / (max_val - min_val) * (target_max - target_min) + target_min)

def plot_coordinates(stdscr):
    curses.curs_set(0)  # Hide the cursor
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    
    # Get min and max for normalization
    min_x, max_x = min(x_values), max(x_values)
    min_y, max_y = min(y_values), max(y_values)
    
    # Avoid division by zero
    if min_x == max_x:
        max_x += 1
    if min_y == max_y:
        max_y += 1
    
    for x, y in zip(x_values, y_values):
        screen_x = normalize(x, min_x, max_x, 1, width - 2)
        screen_y = normalize(y, min_y, max_y, 1, height - 2)
        try:
            stdscr.addch(screen_y, screen_x, '*')
        except curses.error:
            pass  # Ignore errors when trying to plot outside boundaries
    
    stdscr.refresh()
    stdscr.getch()  # Wait for user input before exiting

# Run the curses application
curses.wrapper(plot_coordinates)