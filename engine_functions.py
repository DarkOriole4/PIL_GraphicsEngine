from __init__ import render_res, upscale_res
from tkinter import *
import numpy

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
    ##CALCULATE SCREEN COORDINATES
    FOCAL = 3
    SCALE_FACTOR = 20

    projected_verts = []
    for vertex in vertex_table:
        screen_x = (FOCAL * vertex[0]) / (FOCAL + vertex[2]) * SCALE_FACTOR
        screen_y = (FOCAL * vertex[1]) / (FOCAL + vertex[2]) * SCALE_FACTOR

        #format the coordinates to the correct system
        screen_x = int((screen_x + img.width / (2*UPSCALE_RATIO)) * UPSCALE_RATIO)
        screen_y = int((screen_y + img.width / (2*UPSCALE_RATIO)) * UPSCALE_RATIO)

        projected_vert = (screen_x, screen_y)
        projected_verts.append(projected_vert)

    ##DRAW THE WIREFRAME
    for edge in edge_table:
        a = edge[0]
        b = edge[1]

        draw_line(img, projected_verts[a], projected_verts[b], color)
        img.putpixel(projected_verts[a], (0, 0, 0))
        img.putpixel(projected_verts[b], (0, 0, 0))



def import_model(filename):
    file = open(filename, "r")

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