# To generate 3d and 2d (transformed) coordinates for use by plot.
from sys import argv
from math import sqrt
#import random

MYPOS_X = 32
MYPOS_Y = 32
MYPOS_Z = 32

GRID_WIDTH = 64
GRID_HEIGHT = 64
GRID_DEPTH = 64
GRID_BOX = 16

#'''These constants determine the resolution of fill of a GRID_BOX'''
GRID_Z_INC_MIN = 1
GRID_Y_INC_MIN = 1
GRID_X_INC_MIN = 1


#'''These constants define how quickly the major coordinates are navigated'''
grid_Z_inc = GRID_BOX
grid_X_inc = GRID_BOX
grid_Y_inc = GRID_BOX

FILENAME3D = 'plot_data_3d.csv'
PLOTDATA3D_FILE = open(FILENAME3D, 'w')
PLOTDATA3D_FILE.truncate()

FILENAME2D = 'plot_data_2d.csv'
PLOTDATA2D_FILE = open(FILENAME2D, 'w')
PLOTDATA2D_FILE.truncate()

def print_grid_xyz(x, y, z):
    print ("%3d,%3d,%3d" % (x, y, z))

def write_grid_xyz(x, y, z):
    data = """\n%3d,%3d,%3d""" % (x, y, z)
    PLOTDATA3D_FILE.write(data)

def write_grid2d_xyz(x, y):
    data = """\n%3d,%3d,%3d""" % (x, y, 0)
    PLOTDATA2D_FILE.write(data)

def write_grid_box(pg_x, pg_y, pg_z):
    for z in range(pg_z, pg_z + grid_Z_inc, GRID_Z_INC_MIN):

        for y in range (pg_y, pg_y + grid_Y_inc, GRID_Y_INC_MIN):

            for x in range (pg_x, pg_x + grid_X_inc, GRID_X_INC_MIN):

# Determine what pixel to write to form an empty box
# 1st condition successfully draws front and back faces of box
# 2nd condition draws top and bottom
# 3rd condition draws the sizes
                if (z == pg_z or (z == pg_z + grid_Z_inc - GRID_Z_INC_MIN)) \
                or ((z > pg_z) > 0 and (y == pg_y or y == pg_y + grid_Y_inc - GRID_Y_INC_MIN)) \
                or (z > pg_z and (x == pg_x or x == pg_x + grid_X_inc - GRID_X_INC_MIN)):

# Adjust coordinates for supplied position
                    rel_x = x - MYPOS_X
                    rel_y = y - MYPOS_Y
                    rel_z = z - MYPOS_Z
                    write_grid_xyz(rel_x, rel_y, rel_z)

# Calculate 3d to 2d coordinates and add in perspective
                    rel_xy_SQRT=sqrt(rel_x **2 + rel_y **2)
                    rel_xyz_SQRT=sqrt(rel_x **2 + rel_y **2 + rel_z **2)
#                    if rel_xyz_SQRT != 0 and rel_z >=0 :
                    if rel_xyz_SQRT != 0:
                        depthRatio = rel_xy_SQRT / rel_xyz_SQRT
                        per_x = int(rel_x * depthRatio)
                        per_y = int(rel_y * depthRatio)
                        print("%4d %4d %4d - %4d %4d - %3.4f %3.4f %3.4f" % (rel_x, rel_y, rel_z, per_x, per_y, rel_xy_SQRT, \
                        rel_xyz_SQRT, depthRatio))
                        write_grid2d_xyz(per_x, per_y)

grid_X = 0
grid_Y = 0
grid_Z = 0

PLOTDATA3D_FILE.write("X,Y,Z")
PLOTDATA2D_FILE.write("X,Y,Z")
write_grid_xyz(0, 0, 0)
write_grid2d_xyz(0,0)

#'''Working the Z plane'''
while grid_Z < GRID_DEPTH:
    grid_Y = 0
    Z_switch = ((int(grid_Z / GRID_BOX)) % 2)

#'''Working the Y plane'''
    while grid_Y < GRID_HEIGHT:
        grid_X = 0
        Y_switch = ((int(grid_Y / GRID_BOX)) % 2)
#'''Working the X plane'''
        while grid_X < GRID_WIDTH:
            X_switch = ((int(grid_X / GRID_BOX)) % 2)

#''' Determine if these coordinates represents the corner of a box to be printed'''
            if (Z_switch ^ Y_switch ^ X_switch):
                write_grid_box(grid_X, grid_Y, grid_Z)

#'''Move to the next X grid point'''
            grid_X += grid_X_inc
#'''Move to the next Y grid point'''
        grid_Y += grid_Y_inc
#'''Move to the next Z grid point'''
    grid_Z += grid_Z_inc

PLOTDATA3D_FILE.close()
