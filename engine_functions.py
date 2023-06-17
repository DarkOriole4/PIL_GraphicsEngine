from __init__ import render_res, upscale_res, UPSCALE_RATIO
from tkinter import *
import numpy
from math import tan, radians, cos, sin
from numba import jit, cuda
import colorsys
from PIL import Image



@jit(target_backend="cuda")
def draw_frame(arr, frame): #input needs to be array for the GPU, output is array too
    for x in range(render_res):
        for y in range(render_res):
            uv = [(x/render_res - 0.5) * 2, (y/render_res - 0.5) * 2] # normalise coordinates (from -1 to 1)

            center = [0, 0]  # the center of the screen
            speed = -0.1
            freq = 14
            fxcolor = [102, 71, 255] #effects color

            d = (dist(center, uv) - 0.49)* numpy.exp(-dist(center, uv))  # create sdf of a circle
            d = sin(d*freq + (frame * speed)) / freq # add multiple rings and motion
            d = abs(d)
            if d != 0:
                d = 0.015 / d # invert and add glow
            d = smoothstep(0, 1, d) # smooth out artifacts and edges
            color = [val*d for val in fxcolor]

            arr[x,y] = color #this line sets the RGB color of a given x,y pixel
    return arr


#@jit(target_backend="cuda")  # disabled for now
def draw_line(arr, start, end, color):
    if start[0]<0 or start[1]<0 or start[0]>render_res or start[1]>render_res:
        raise ValueError('Invalid start coordinate')

    elif end[0]<0 or end[1]<0 or end[0]>render_res or end[1]>render_res:
        raise ValueError('Invalid end coordinate')

    #swap x and y coordinates, because the lines looked
    # rotated 90 deg for some reason
    temp = start[1]
    start[1] = start[0]
    start[0] = -temp

    temp = end[1]
    end[1] = end[0]
    end[0] = -temp

    #FIX DRAW DIRECTION
    if start[0] > end[0]: #if right-to-left, swap start with end
        temp = end
        end = start
        start = temp
   
    if start[0] != end[0]: #non-vertical line
        cursor = numpy.array(start)
        slope = (end[1] - start[1]) / numpy.abs(end[0] - start[0])
        stepval = abs(int(slope)) #slope's whole component
        if slope == 0 or is_integer(slope):       #
            slope_mod = 0                         #
        elif slope < 1 and slope > -1:            #
            slope_mod = 1 / slope                 # slope_mod: the frequency at which an additional px needs to be added
        else:                                     #
            slope_mod = 1 / (slope - int(slope))  #

        arr[start[0], start[1]] = color #put first pixel at start
        count1 = stepval
        count2 = 1
        while cursor[0] < end[0]: #REPEAT UNTIL THE CURSOR REACHES THE END       
            cursor[0] += 1

            if slope != 0 and (slope < 1 and slope > -1) and ((count2 + 1) % slope_mod >= 1 or (count2 + 1) % slope_mod <= -1): #ok, I give up
                arr[cursor[0], cursor[1]] = color # fill in the steps
            
            count1 = stepval
            if slope != 0: #not horizontal line
                while count1 > 0:
                    if slope > 0:
                        cursor[1] += 1
                    else:
                        cursor[1] -= 1

                    arr[cursor[0], cursor[1]] = color
                    count1 -= 1
                # END OF STEP
                if slope_mod != 0:
                    count2 = (count2 + 1) % slope_mod
                    
                if count2 < 1 and count2 > -1: # add 1px if needed
                    if slope > 0:
                        cursor[1] += 1
                    else:
                        cursor[1] -= 1

                    arr[cursor[0], cursor[1]] = color
            else:
                arr[cursor[0], cursor[1]] = color

          
    elif start[0] == end[0]: # vertical line
        cursor = numpy.array(start)
        v_steps = abs(end[1] - start[1])
        
        v_count = 0
        if start[1] < end[1]: # top-to-bottom
            while v_count < v_steps:
                arr[cursor[0], start[1]+v_count] = color
                v_count += 1
        else: # bottom-to-top
            while v_count < v_steps:
                arr[cursor[0], start[1]-v_count] = color
                v_count += 1

    return arr



def draw_wireframe(arr, vertex_table, edge_table, color):
    ## SET IMPORTANT VARIABLES
    autozoom = True
    if autozoom == True:
        fovy = 0.99157**(render_res-750) + 22 # The angle between the upper and lower sides of the viewing frustum (acts like zoom)
    else:
        fovy = 40
    aspect = 1  # The aspect ratio of the viewing window.
    near = 0.1  # Number Distance to the near clipping plane along the -Z axis
    far = 100.0  # Number Distance to the far clipping plane along the -Z axis
    top = near * tan(radians(fovy / 120))
    bottom = -top
    right = top * aspect
    left = -top
    margin = 1

    # The perspective transformation matrix
    P_MATRIX = [[2*near/(right-left),         0,                       0,           -near*(right+left)/(right-left)],
                [       0,            2*near/(top-bottom),             0,           -near*(top+bottom)/(top-bottom)],
                [       0,                    0,            -(far+near)/(far-near),      2*far*near/(near-far)     ],
                [       0,                    0,                      -1,                           0              ]]

    ##CALCULATE SCREEN COORDINATES
    projected_verts = []
    for vertex in vertex_table:
        vertex = list(vertex)
        vertex.append(1)
        #format the coordinates to the correct system
        projected_vert = numpy.matmul(vertex, P_MATRIX)
        projected_verts.append(projected_vert)

    ##DRAW THE WIREFRAME
    edge_index = 0
    for edge in edge_table:
        a = edge[0]
        b = edge[1]

        #center the model in the middle of the screen
        startpoint = (projected_verts[a] + render_res / (2*UPSCALE_RATIO) * UPSCALE_RATIO)
        endpoint = (projected_verts[b] + render_res / (2*UPSCALE_RATIO) * UPSCALE_RATIO)

        # restrict the coordinates to 2D and clip to the screensize
        startpoint = numpy.clip(startpoint[0:2], 0, render_res - margin)
        endpoint = numpy.clip(endpoint[0:2], 0, render_res - margin)

        #round to int
        startpoint = [int(coor) for coor in startpoint]
        endpoint = [int(coor) for coor in endpoint]

        #find the edges approximate location 0 - 1 (optional)
        loc_x = int((startpoint[0] + endpoint[0]) / 2) / render_res
        # loc_y = int((startpoint[1] + endpoint[1]) / 2)

        new_color = colorsys.hsv_to_rgb(loc_x*360 / 360, 1, 1) #set the color accordingly
        new_color = tuple([int(val * 255) for val in new_color]) #reformat

        arr = draw_line(arr, startpoint, endpoint, new_color)
        edge_index += 1

    img = Image.fromarray(arr)  # back to the CPU
    return img



def rotate_mesh(vertex_table, angle):
    y_rotation_matrix = [[cos(angle),  0, sin(angle)],
                        [     0,       1,     0     ],
                        [-sin(angle),  0, cos(angle)]]
    
    rotated_table = []
    for vertex in vertex_table:
        rotated_table.append(numpy.matmul(vertex, y_rotation_matrix))
    return rotated_table



def import_model(filepath):
    file = open(filepath, "r")

    vertex_table = []
    edge_table = []

    for line in file:
        line = line.rstrip("\n")
        if line != '':  # detect the separator (the empty line)
            values = line.split(" ")  # convert to list

            for i in range(len(values)):
                values[i] = float(values[i])  # convert str to float

            values = tuple(values)  # convert to tuple
            vertex_table.append(values)
        else:
            for line in file:
                values = line.split(" ")  # convert to list

                for i in range(len(values)):
                    values[i] = int(values[i])  # convert str to float

                values = tuple(values)  # convert to tuple
                edge_table.append(values)
    file.close()
    return vertex_table, edge_table



def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()

def convert_img2arr(img):
    arr = numpy.array(img)
    #arr = numpy.rot90(arr, k=1, axes=(0, 1))
    return arr

@jit(target_backend="cuda")
def dist(p1, p2):
    return numpy.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

@jit(target_backend="cuda")
def step(threshold, val):
    if val >= threshold:
        return 1
    else:
        return 0

@jit(target_backend="cuda")
def smoothstep(low, high, val):
    #return numpy.tanh(val / threshold)
    #return 1 / (1 + (numpy.e ** (-val / threshold)))
    if low >= high:
        return None
    else:
        t = clamp((val - low) / (high - low), 0, 1)
        return  t * t * (3 - 2 * t)

@jit(target_backend="cuda")
def clamp (val, low, high):
    if val < low:
        return low
    elif val > high:
        return high
    else:
        return val