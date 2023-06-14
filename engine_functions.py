from __init__ import render_res, upscale_res
from tkinter import *
import numpy
from math import tan, radians, cos, sin

UPSCALE_RATIO = render_res / 64


def draw_line(img, start, end, color):
    if start[0]<0 or start[1]<0 or start[0]>render_res or start[1]>render_res:
        raise ValueError('Invalid start coordinate')
    elif end[0]<0 or end[1]<0 or end[0]>render_res or end[1]>render_res:
        raise ValueError('Invalid end coordinate')


    #FIX DRAW DIRECTION
    if start[0] > end[0]: #if right-to-left, swap start with end
        temp = end
        end = start
        start = temp
   
    if start[0] != end[0]: #non-vertical line
        cursor = list(start)
        slope = (end[1] - start[1]) / numpy.abs(end[0] - start[0])
        stepval = abs(int(slope)) #slope's whole component
        if slope < 1 and slope > -1:              #
            slope_mod = 1 / slope                 # slope_mod: the frequency at which an additional px needs to be added
        else:                                     #
            slope_mod = 1 / (slope - int(slope))  #
        
        img.putpixel(start, color) #put first pixel at start
        count1 = stepval
        count2 = 1
        while cursor[0] < end[0]: #REPEAT UNTIL THE CURSOR REACHES THE END       
            cursor[0] += 1

            if (slope < 1 and slope > -1) and ((count2 + 1) % slope_mod >= 1 or (count2 + 1) % slope_mod <= -1): #ok, I give up
                img.putpixel(cursor, color) # fill in the steps
            
            count1 = stepval
            if slope != 0: #not horizontal line
                while count1 > 0:
                    if slope > 0:
                        cursor[1] += 1
                    else:
                        cursor[1] -= 1

                    img.putpixel(cursor, color)
                    count1 -= 1
                # END OF STEP
                count2 = (count2 + 1) % slope_mod
                    
                if count2 < 1 and count2 > -1: # add 1px if needed
                    if slope > 0:
                        cursor[1] += 1
                    else:
                        cursor[1] -= 1

                    img.putpixel(cursor, color)
            else:
                img.putpixel(cursor, color)

          
    elif start[0] == end[0]: # vertical line
        cursor = list(start)
        v_steps = abs(end[1] - start[1])
        
        v_count = 0
        if start[1] < end[1]: # top-to-bottom
            while v_count < v_steps:
                img.putpixel((cursor[0], start[1]+v_count), color)
                v_count += 1
        else: # bottom-to-top
            while v_count < v_steps:
                img.putpixel((cursor[0], start[1]-v_count), color)
                v_count += 1



def draw_wireframe(img, vertex_table, edge_table, color):
    ## SET IMPORTANT VARIABLES
    fovy = 90 # The angle between the upper and lower sides of the viewing frustum
    aspect = img.width / img.height  # The aspect ratio of the viewing window.
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
        # screen_x = int((screen_x + img.width / (2*UPSCALE_RATIO)) * UPSCALE_RATIO)
        # screen_y = int((screen_y + img.width / (2*UPSCALE_RATIO)) * UPSCALE_RATIO)
        projected_vert = numpy.matmul(vertex, P_MATRIX)
        projected_verts.append(projected_vert)

    ##DRAW THE WIREFRAME
    for edge in edge_table:
        a = edge[0]
        b = edge[1]

        startpoint = (projected_verts[a] + img.width / (2*UPSCALE_RATIO) * UPSCALE_RATIO)
        endpoint = (projected_verts[b] + img.width / (2*UPSCALE_RATIO) * UPSCALE_RATIO)

        # restrict the coordinates to 2D and clip to the screensize
        startpoint = numpy.clip(startpoint[0:2], 0, render_res - margin)
        endpoint = numpy.clip(endpoint[0:2], 0, render_res - margin)

        #round to int
        startpoint = [int(coor) for coor in startpoint]
        endpoint = [int(coor) for coor in endpoint]

        draw_line(img, startpoint, endpoint, color)



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