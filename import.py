import math
import curses
import time
import pandas as pd
import random


def import_object(file_path, off_x, off_y, off_z):
    global x_object, y_object, z_object
    data = pd.read_csv(file_path)
    # Ensure the columns are named X, Y, Z
    if not {'X', 'Y', 'Z'}.issubset(data.columns):
        raise ValueError(f"The CSV file: {file_path} must have 'X', 'Y', 'Z' columns.")

    # Filter out rows where Z < 0
    #data = data[data['Z'] >= 0]

    # Extract coordinates
    x_object = data['X'] + off_x
    y_object = data['Y'] + off_y
    z_object = data['Z'] + off_z

def XYZ_ROTATION(theta, p1, p2):
    # For rotation along the Z, X or Y axis, supply the required values for p1 & p2 and
    #  the returned values are for those axis, i.e.   Z = xp  yp,  X = zp  yp, Y = xp zp
    theta_rads = math.radians(theta)
    p1_prime = p1 * math.cos(theta_rads) - p2 * math.sin(theta_rads)
    p2_prime = p1 * math.sin(theta_rads) + p2 * math.cos(theta_rads)                    
    return p1_prime, p2_prime

def transform_object(TO_INC):
    global xy_plane5
    for vector in range(0, len( x_object ), TO_INC ):
        xo, yo, zo = x_object[vector], y_object[vector], z_object[vector]

        rel_x = (xo * SCALE_RATIO) - ORIGIN_X
        rel_y = (yo * SCALE_RATIO) - ORIGIN_Y
        rel_z = (zo * SCALE_RATIO) - ORIGIN_Z

        xp, yp = XYZ_ROTATION(z_rotation, rel_x, rel_y)
        zp, yp = XYZ_ROTATION(x_rotation, rel_z, yp)
        xp, zp = XYZ_ROTATION(y_rotation, xp, zp)

        per_x, per_y = perspective_projection(xp, yp, zp)
        per_x += ORIGIN_X
        per_y += ORIGIN_Y

        xy_plane_index = per_x, per_y
        if xy_plane_index not in xy_plane and zp > -100:
            xy_plane.append((per_x, per_y))

def perspective_projection(xp, yp, zp):
    pp_x = int( ( xp / ( (zp / 100) + 1) ) / 2 )
    pp_y = int( ( yp / ( (zp / 100) + 1) ) / 2 )
    return pp_x, pp_y

def draw_screen():
    global x_values, y_values
    x_values , y_values = zip(*xy_plane) # Create x and y lists from xy_plane
 #   x_values = [ x + BASE_ORIGIN_X for x in x_values ] # Add back in the origin
 #   y_values = [ y + BASE_ORIGIN_Y for y in y_values ] # Add back in the origin
    curses.wrapper(plot_coordinates)

def plot_coordinates(stdscr):
    curses.curs_set(0)  # Hide the cursor
    stdscr.erase()
    height, width = stdscr.getmaxyx()
    screen_center_x = width / 2
    screen_centre_y = height / 2
    
    min_x, min_y = 1, 1
    max_x, max_y = width, height
    for x, y in zip(x_values, y_values):
        screen_x = int( screen_center_x + (x * SCREEN_RATIO) )
        screen_y = int( screen_centre_y + (y * SCREEN_RATIO) )
        if not (screen_x < 0 or screen_x > width - 1 or screen_y < 0 or screen_y > height - 1):
            try:
                stdscr.addch(screen_y, screen_x, chr(0x2588))                
            except curses.error:
                pass  # Ignore errors when trying to plot outside boundaries

    stdscr.refresh()
    time.sleep(.1)
    
    #stdscr.getch()  # Wait for user input before exiting
    stdscr.erase()

#   ___ _   _ ___ _____ 
#   |_ _| \ | |_ _|_   _|
#    | ||  \| || |  | |  
#    | || |\  || |  | |  
#   |___|_| \_|___| |_|  
#                     


x_object, y_object, z_object = [], [], []
file_path = "object_data.csv"
import_object(file_path,-0, 0, -12)

SCREEN_RATIO = 1
SCALE_RATIO = 3
TO_INC = 20

GRID_RATIO = 4
GRID_WIDTH = 64 * GRID_RATIO
GRID_HEIGHT =32 * GRID_RATIO
GRID_DEPTH = 16 * GRID_RATIO

ORIGIN_X = GRID_WIDTH / 2
ORIGIN_Y = GRID_HEIGHT / 2
ORIGIN_Z = GRID_DEPTH / 2

ORIGIN_X = 0
ORIGIN_Y = 0
ORIGIN_Z = 0


x_rotation = 0
x_rotation_inc = int(random.random()*3)
y_rotation = 0
y_rotation_inc = int(random.random()*4)
z_rotation = 0
z_rotation_inc = int(random.random()*5)


#x_rotation = 5
#x_rotation_inc = 0
#y_rotation = 0
#y_rotation_inc = 7
#z_rotation = 45
#z_rotation_inc = 4

while True:
    xy_plane = []
    transform_object(TO_INC)
    draw_screen()

    x_rotation += x_rotation_inc
    y_rotation += y_rotation_inc
    z_rotation += z_rotation_inc