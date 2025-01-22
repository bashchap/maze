from sys import argv
#import random

GRID_WIDTH = 32
GRID_HEIGHT = 32
GRID_DEPTH = 32
GRID_BOX = 16
#'''These constants determine the resolution of fill of a GRID_BOX'''
GRID_Z_INC_MIN = 2
GRID_Y_INC_MIN = 2
GRID_X_INC_MIN = 2
#'''These constants define how quickly the major coordinates are navigated'''
grid_Z_inc = GRID_BOX
grid_X_inc = GRID_BOX
grid_Y_inc = GRID_BOX

FILENAME = 'plot_data.csv'
PLOTDATA_FILE = open(FILENAME, 'w')
PLOTDATA_FILE.truncate()
PLOTDATA_FILE.write("X,Y,Z")

def print_grid_xyz(x, y, z, Xs, Ys, Zs, YorN):
    print ("%3d,%3d,%3d - %1s %1s %1s : %1s" % (x, y, z, Xs, Ys, Zs, YorN))

def write_grid_xyz(x, y, z):
    data = """\n%3d,%3d,%3d""" % (x, y, z)
    PLOTDATA_FILE.write(data)
#'''FUNCTION: to fill in a box'''
#'''This needs to be modified to only fill in the faces, not the 'contents' '''


def write_grid_box(pg_x, pg_y, pg_z):
#    print_grid_xyz(pg_x, pg_y, pg_z, 9, 9, 9, "Y")
#    print ("z is now %d going to %d in steps of %d" % (pg_z, pg_z + grid_Z_inc, GRID_Z_INC_MIN))

# Step 0 - draw first face
    for z in range(pg_z, pg_z + grid_Z_inc, GRID_Z_INC_MIN):
        print("z is %d, max = %d, inc = %d" % (z, pg_z + grid_Z_inc, GRID_Z_INC_MIN))
#        print ("y is now %d going to %d in steps of %d" % (pg_y, pg_y + grid_Y_inc, GRID_Y_INC_MIN))
        for y in range (pg_y, pg_y + grid_Y_inc, GRID_Y_INC_MIN):
#            print ("x is now %d going to %d in steps of %d" % (pg_x, pg_x + grid_X_inc, GRID_X_INC_MIN))
            for x in range (pg_x, pg_x + grid_X_inc, GRID_X_INC_MIN):
#                if (Z_Step == 0 or (Z_Step == pg_z + grid_Z_inc - GRID_Z_INC_MIN)) or (Z_Step > 0 and Y_Step == 0) :
# Line below successfully draws front and back faces of box
#                if (Z_Step == 0 or (Z_Step == pg_z + grid_Z_inc - GRID_Z_INC_MIN)):
                if (z == pg_z or (z == pg_z + grid_Z_inc - GRID_Z_INC_MIN)) or ((z > pg_z) > 0 and (y == pg_y or y == pg_y + grid_Y_inc - GRID_Y_INC_MIN) ):
                    write_grid_xyz(x, y, z)


#                print_grid_xyz(x, y, z, 9, 9, 9, "Y")
grid_X = 0
grid_Y = 0
grid_Z = 0



#''' Creates random major jump movements'''
#grid_Z_inc = random.randint(1, GRID_DEPTH)
#grid_X_inc = random.randint(1, GRID_WIDTH)
#grid_Y_inc = random.randint(1, GRID_HEIGHT)



#'''Working the Z plane'''
while grid_Z < GRID_DEPTH:
    grid_Y = 0
    Z_switch = ((int(grid_Z / GRID_BOX)) % 2)

#'''Working the Y plane'''
    while grid_Y < GRID_HEIGHT:
        grid_X = 0
        Y_switch = ((int(grid_Y / GRID_BOX)) % 2)
#        GRID_BOX = random.randint (4, 32)
#'''Working the X plane'''
        while grid_X < GRID_WIDTH:
            X_switch = ((int(grid_X / GRID_BOX)) % 2)

#''' Determine if these coordinates represents the corner of a box to be printed'''
            if (Z_switch ^ Y_switch ^ X_switch):
#                write_grid_xyz(grid_X, grid_Y, grid_Z)
                write_grid_box(grid_X, grid_Y, grid_Z)

#'''Move to the next X grid point'''
            grid_X += grid_X_inc
#'''Move to the next Y grid point'''
        grid_Y += grid_Y_inc
#'''Move to the next Z grid point'''
    grid_Z += grid_Z_inc

PLOTDATA_FILE.close()
