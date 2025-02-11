import csv

def read_object():
    global xy_plane
# Read the CSV file
    with open("duff.csv", mode="r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            xy_plane.append((float(row[0]), float(row[1]), float(row[2])))

def draw_screen():
    global x_values, y_values
    x_values , y_values = zip(*xy_plane) # Create x and y lists from xy_plane
    curses.wrapper(plot_coordinates)

def plot_coordinates(stdscr):
    curses.curs_set(0)  # Hide the cursor
    stdscr.erase()
    height, width = stdscr.getmaxyx()
    screen_center_x = width / 2
    screen_centre_y = height / 2
    
    min_x, min_y = 1, 1
    max_x, max_y = width - 1, height - 1
    
    for x, y in zip(x_values, y_values):
        screen_x = int( screen_center_x + x )
        screen_y = int( screen_centre_y + y )
        if not (screen_x < 0 or screen_x >= width - 1 or screen_y < 0 or screen_y >= height - 1):
            try:
                stdscr.addch(screen_y, screen_x, '*')
            except curses.error:
                pass  # Ignore errors when trying to plot outside boundaries

    stdscr.refresh()
    #time.sleep(10)
    stdscr.getch()  # Wait for user input before exiting

# Initialize the list to hold the coordinate tuples
xy_plane = []
read_object()
draw_screen()


