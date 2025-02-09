# To generate 3d and 2d (transformed) coordinates for use by plot.
from sys import argv
from math import sqrt
import curses
import time
#import random

xy_plane = []
xy_dups = 0
xy_total = 0
xyz_total = 0
current_frame = 0

GRID_RATIO = 32

GRID_WIDTH = 32 * GRID_RATIO
GRID_HEIGHT = 16 * GRID_RATIO
GRID_DEPTH = 24 * GRID_RATIO

GRID_BOX = 8 * GRID_RATIO

GRID_BOX_X = 8 * GRID_RATIO
GRID_BOX_Y = 8 * GRID_RATIO
GRID_BOX_Z = 8 * GRID_RATIO

BASE_ORIGIN_X = GRID_WIDTH / 2 + GRID_BOX_X / 2
BASE_ORIGIN_Y = GRID_HEIGHT / 2 + GRID_BOX_Y / 2
BASE_ORIGIN_Z = GRID_BOX_Z

#'''These constants determine the resolution of fill of a GRID_BOX'''
GRID_Z_INC_MIN = 4 
GRID_Y_INC_MIN = 1
GRID_X_INC_MIN = 1


#'''These constants define how quickly the major coordinates are navigated'''
GRID_X_INC_MAJ = GRID_BOX_X
GRID_Y_INC_MAJ = GRID_BOX_Y
GRID_Z_INC_MAJ = GRID_BOX_Z



def print_grid_xyz(x, y, z):
    print ("%3d,%3d,%3d" % (x, y, z))

def write_grid3d_xyz(x, y, z):
    data = """\n%3d,%3d,%3d""" % (x, y, z)
    PLOTDATA3D_FILE.write(data)

def write_grid2d_xyz(x, y):
    data = """\n%3d,%3d,%3d""" % (x, y, 0)
    PLOTDATA2D_FILE.write(data)

def write_grid_box(wgb_x, wgb_y, wgb_z):
    global ORIGIN_Z, ORIGIN_Y, ORIGIN_X
    global xy_plane, xy_dups, xy_total, xyz_total, current_frame
    for z in range(wgb_z, wgb_z + GRID_Z_INC_MAJ, GRID_Z_INC_MIN):
        z_edge = (z == wgb_z) or (z == wgb_z + GRID_Z_INC_MAJ - GRID_Z_INC_MIN)

        for y in range (wgb_y, wgb_y + GRID_Y_INC_MAJ, GRID_Y_INC_MIN):
            y_edge = (y == wgb_y) or (y == wgb_y + GRID_Y_INC_MAJ - GRID_Y_INC_MIN)

            for x in range (wgb_x, wgb_x + GRID_X_INC_MAJ, GRID_X_INC_MIN):
                x_edge = (x == wgb_x) or (x == wgb_x + GRID_X_INC_MAJ - GRID_X_INC_MIN)

# Determine what pixel to write to form an empty box (faces filled)
# 1st condition successfully draws front and back faces of box
# 2nd condition draws top and bottom
# 3rd condition draws the sizes
#                if (z_edge) \
#                or ((not z_edge) and (y_edge)) \
#                or (not z_edge) and (x_edge):

# Determine what pixel to write to form the edges of a box
# Conditions determine if when an edge is visible so can plot an outline
                if (z_edge and (y_edge or x_edge)) or \
                   ((not z_edge) and (x_edge and y_edge)):
                    xyz_total += 1

# Create relative coordinates for supplied position
                    rel_x = x - ORIGIN_X
                    rel_y = y - ORIGIN_Y
                    rel_z = z - ORIGIN_Z

# Write 2D & 3D coordinates only for first frame
                    if current_frame != -1 :
                        write_grid3d_xyz(rel_x, rel_y, rel_z)

# Calculate 3d to 2d coordinates and add in perspective
#                    rel_xy_SQR = rel_x **2 + rel_y **2
#                    rel_xy_SQRT = sqrt(rel_xy_SQR)
#                    rel_xyz_SQR = rel_xy_SQR + rel_z **2
#                    rel_xyz_SQRT = sqrt(rel_xyz_SQR)

                    if  rel_z > 0 and rel_z < ( rel_z + GRID_BOX_Z * 8) :
                        xy_total += 1
                        per_x = int( ( rel_x / ( (rel_z / 100) + 1) ) / 2 )
                        per_y = int( ( rel_y / ( (rel_z / 100) + 1) ) / 2 )

# If a 2D coordinate has previously been calculated skip it, otherwise store the coordinates.
# This is because we've already translated from 3D to 2D so anything else at that coordinate is behind what's
# already been drawn (since we're drawing from the direction we're facing forward only).
                        xy_plane_index = per_x, per_y
                        if xy_plane_index not in xy_plane:
                            xy_plane.append((per_x, per_y))
                            if current_frame != -1:
                                write_grid2d_xyz(per_x, per_y)
                        else:
                            xy_dups += 1

def print_debug(frame, x, y, z, rel_x, rel_y, rel_z, rel_xy_SQR, rel_xy_SQRT, rel_xyz_SQR, rel_xyz_SQRT, depthRatio, per_x, per_y, screen_x, screen_y):
    print(f"{frame},{x},{y},{z},{rel_x},{rel_y},{rel_z},{rel_xy_SQR},{rel_xy_SQRT},{rel_xyz_SQR},{rel_xyz_SQRT},{depthRatio},{per_x},{per_y},{screen_x},{screen_y}")

def print_debug_header():
    print(f"frame, x, y, z, rel_x, rel_y, rel_z, rel_xy_SQR, rel_xy_SQRT, rel_xyz_SQR, rel_xyz_SQRT, depthRatio_x, per_x, per_y, screen_x, screen_y")

def plot_char(stdscr, x, y):
    stdscr.addch(y, x, "#")

def show_screen(stdscr):
    stdscr.refresh()

def clear_screen(stdscr):
    stdscr.clear()

def screen_wait(stdscr):
    stdscr.getch()

def print_totals():
    global xy_total, xy_dups
    print("Total 3D points: %d" % xyz_total)
    print("Total 2D points: %d" % xy_total)
    print("Total 2D duplicates: %d" % xy_dups)

def draw_screen():
    global x_values, y_values
    x_values , y_values = zip(*xy_plane) # Create x and y lists from xy_plane
#    x_values = [ x + BASE_ORIGIN_X for x in x_values ] # Add back in the origin
#    y_values = [ y + BASE_ORIGIN_Y for y in y_values ] # Add back in the origin

    curses.wrapper(plot_coordinates)

def normalize(value, min_val, max_val, target_min, target_max):
    """Normalize values to fit within target range."""
    return int((value - min_val) / (max_val - min_val) * (target_max - target_min) + target_min)

def plot_coordinates(stdscr):
    curses.curs_set(0)  # Hide the cursor
    stdscr.erase()
    height, width = stdscr.getmaxyx()
    screen_center_x = width / 2
    screen_centre_y = height / 2
    
    # Get min and max for normalization
    # min_x, max_x = min(x_values), max(x_values)
    # min_y, max_y = min(y_values), max(y_values)
    
    min_x, min_y = 1, 1
    max_x, max_y = width - 1, height - 1
    
    # Avoid division by zero
    #if min_x == max_x:
    #    max_x += 1
    #if min_y == max_y:
    #    max_y += 1
    
    for x, y in zip(x_values, y_values):
#        screen_x = normalize(x, min_x, max_x, 1, width - 2)
#        screen_y = normalize(y, min_y, max_y, 1, height - 2)
        screen_x = int( screen_center_x + x )
        screen_y = int( screen_centre_y + y )
        if not (screen_x < 0 or screen_x >= width - 1 or screen_y < 0 or screen_y >= height - 1):
            try:
                stdscr.addch(screen_y, screen_x, '*')
            except curses.error:
                pass  # Ignore errors when trying to plot outside boundaries

    stdscr.refresh()
    #time.sleep(10)
    #stdscr.erase()
    #stdscr.getch()  # Wait for user input before exiting




def walk_the_grid():
    global ORIGIN_Z, ORIGIN_Y, ORIGIN_X
    #'''Working the Z plane'''
    grid_Z = 0
    while grid_Z < GRID_DEPTH:
        grid_Y = 0
        Z_switch = ((int(grid_Z / GRID_Z_INC_MAJ)) % 2)

    #'''Working the Y plane'''
        while grid_Y < GRID_HEIGHT:
            grid_X = 0
            Y_switch = ((int(grid_Y / GRID_Y_INC_MAJ)) % 2)
    #'''Working the X plane'''
            while grid_X < GRID_WIDTH:
                X_switch = ((int(grid_X / GRID_X_INC_MAJ)) % 2)

    #''' Determine if these coordinates represents the corner of a box to be printed'''
                if (Z_switch ^ Y_switch ^ X_switch):
                    write_grid_box(grid_X, grid_Y, grid_Z)

    #'''Move to the next X grid point'''
                grid_X += GRID_X_INC_MAJ
    #'''Move to the next Y grid point'''
            grid_Y += GRID_Y_INC_MAJ
    #'''Move to the next Z grid point'''
        grid_Z += GRID_Z_INC_MAJ

#                  _       
#  _ __ ___   __ _(_)_ __  
# | '_ ` _ \ / _` | | '_ \ 
# | | | | | | (_| | | | | |
# |_| |_| |_|\__,_|_|_| |_|



MAX_FRAMES = 256
current_frame = 0
ORIGIN_X = BASE_ORIGIN_X
ORIGIN_Y = BASE_ORIGIN_Y
ORIGIN_Z = BASE_ORIGIN_Z - 128

while current_frame < MAX_FRAMES:
    file_frame = f"{current_frame:04d}"

    FILENAME3D = f"plot_data_3d_{file_frame}.csv"
    PLOTDATA3D_FILE = open(FILENAME3D, 'w')
    PLOTDATA3D_FILE.truncate()

    FILENAME2D = f"plot_data_2d_{file_frame}.csv"
    PLOTDATA2D_FILE = open(FILENAME2D, 'w')
    PLOTDATA2D_FILE.truncate()

    PLOTDATA3D_FILE.write("X,Y,Z")
    PLOTDATA2D_FILE.write("X,Y,Z")
    write_grid3d_xyz(0, 0, 0)
    write_grid2d_xyz(0, 0)

    walk_the_grid()
    draw_screen()

    PLOTDATA2D_FILE.close()
    PLOTDATA3D_FILE.close()
    xy_plane.clear()

    ORIGIN_X += GRID_X_INC_MIN * 1
    ORIGIN_Z += GRID_Z_INC_MIN * 1
    current_frame += 1
    #quit()

print_totals()
