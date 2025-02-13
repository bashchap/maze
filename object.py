# To generate 3d and 2d (transformed) coordinates for use by plot.
from sys import argv
from math import sqrt
import math
import curses
import time
import random

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

#                #print(f"HERE: {x}, {y}, {z}")
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

                    xp, yp = XYZ_ROTATION(z_rotation, rel_x, rel_y)
                    zp, yp = XYZ_ROTATION(x_rotation, rel_z, yp)
                    xp, zp = XYZ_ROTATION(y_rotation, xp, zp)

                    zp += GRID_BOX_Z * 2


# Write 2D & 3D coordinates only for first frame
                    if current_frame != -1 :
                        write_grid3d_xyz(xp, yp, zp)

                    if zp != -999:
                        xy_total += 1
                        per_x = int( ( xp / ( (zp / 100) + 1) ) / 2 )
                        per_y = int( ( yp / ( (zp / 100) + 1) ) / 2 )

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
        screen_x = int( screen_center_x + x )
        screen_y = int( screen_centre_y + y )
        if not (screen_x < 0 or screen_x > width - 1 or screen_y < 0 or screen_y > height - 1):
            try:
                stdscr.addch(screen_y, screen_x, chr(0x2588))                
            except curses.error:
                pass  # Ignore errors when trying to plot outside boundaries

    stdscr.refresh()
    time.sleep(.1)
    
    #stdscr.getch()  # Wait for user input before exiting
    stdscr.erase()




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

def XYZ_ROTATION(theta, p1, p2):
    # For rotation along the Z, X or Y axis, supply the required values for p1 & p2 and
    #  the returned values are for those axis, i.e.:
    #                                                   Z = xp  yp,  X = zp  yp, Y = xp zp
    theta_rads = math.radians(theta)
    p1_prime = p1 * math.cos(theta_rads) - p2 * math.sin(theta_rads)
    p2_prime = p1 * math.sin(theta_rads) + p2 * math.cos(theta_rads)                    
    return p1_prime, p2_prime

#   ___ _   _ ___ _____ 
#   |_ _| \ | |_ _|_   _|
#    | ||  \| || |  | |  
#    | || |\  || |  | |  
#   |___|_| \_|___| |_|  
#                     


GRID_RATIO = 6

GRID_WIDTH = 64 * GRID_RATIO
GRID_HEIGHT =32 * GRID_RATIO
GRID_DEPTH = 16 * GRID_RATIO

GRID_BOX = 32 * GRID_RATIO

GRID_BOX_X =  16 * GRID_RATIO
GRID_BOX_Y =  16 * GRID_RATIO
GRID_BOX_Z =  16 * GRID_RATIO

BASE_ORIGIN_X = GRID_WIDTH / 2
BASE_ORIGIN_Y = GRID_HEIGHT / 2
BASE_ORIGIN_Z = GRID_DEPTH / 2

#'''These constants determine the resolution of fill of a GRID_BOX'''
GRID_Z_INC_MIN = 4
GRID_Y_INC_MIN = 4
GRID_X_INC_MIN = 4

#'''These constants define how quickly the major coordinates are navigated'''
GRID_X_INC_MAJ = GRID_BOX_X
GRID_Y_INC_MAJ = GRID_BOX_Y
GRID_Z_INC_MAJ = GRID_BOX_Z

ORIGIN_X = GRID_WIDTH / 2
ORIGIN_Y = GRID_HEIGHT / 2
ORIGIN_Z = GRID_DEPTH / 2


x_rotation = 0
x_rotation_inc = int(random.random()*3)
y_rotation = 0
y_rotation_inc = int(random.random()*4)
z_rotation = 0
z_rotation_inc = int(random.random()*5)

#                  _       
#  _ __ ___   __ _(_)_ __  
# | '_ ` _ \ / _` | | '_ \ 
# | | | | | | (_| | | | | |
# |_| |_| |_|\__,_|_|_| |_|

xy_plane = []
xy_dups = 0
xy_total = 0
xyz_total = 0
current_frame = 0

MAX_FRAMES, current_frame = 512, 0

PLOT_DATA_DIR = "./plotdata"
while current_frame < MAX_FRAMES:
    file_frame = f"{current_frame:04d}"

#    print(f"Current frame: {current_frame}   Z: {ORIGIN_Z}")

    FILENAME3D = f"{PLOT_DATA_DIR}/plot_data_3d_{file_frame}.csv"
    PLOTDATA3D_FILE = open(FILENAME3D, 'w')
    PLOTDATA3D_FILE.truncate()

    FILENAME2D = f"{PLOT_DATA_DIR}/plot_data_2d_{file_frame}.csv"
    PLOTDATA2D_FILE = open(FILENAME2D, 'w')
    PLOTDATA2D_FILE.truncate()

    PLOTDATA3D_FILE.write("X,Y,Z")
    PLOTDATA2D_FILE.write("X,Y,Z")
    #write_grid3d_xyz(0, 0, 0)
    #write_grid2d_xyz(0, 0)

    walk_the_grid()
    draw_screen()

    PLOTDATA2D_FILE.close()
    PLOTDATA3D_FILE.close()
    xy_plane.clear()

#    ORIGIN_X += GRID_X_INC_MIN * 1
#    ORIGIN_Z += GRID_Z_INC_MIN * 1
    current_frame += 1
    x_rotation += x_rotation_inc
    y_rotation += y_rotation_inc
    z_rotation += z_rotation_inc
    #quit()

# print_totals()
