from __init__ import render_res, img

from tkinter import *
import numpy


def draw_line(img, start, end, color):
    if start[0]<0 or start[1]<0 or start[0]>render_res or start[1]>render_res:
        raise ValueError('Invalid start coordinate')
    elif end[0]<0 or end[1]<0 or end[0]>render_res or end[1]>render_res:
        raise ValueError('Invalid end coordinate')
################################################################################    
    #FIX DRAW DIRECTION
    if start[0] > end[0]: #if right-to-left, swap start with end
        temp = end
        end = start
        start = temp
    
    if start[1] > end[1]: #if bottom-to-top, swap top with bottom
        temp = end
        end = start
        start = temp
################################################################################      
    elif start[0] != end[0]: #non-vertical line
        cursor = list(start)
        slope = numpy.abs(end[1] - start[1]) / numpy.abs(end[0] - start[0])
        stepval = int(slope) #slope's whole component
        if slope < 1 and slope > -1:             #
            slope_mod = slope ** -1              # slope_mod: the frequency at which an additional px needs to be added
        else:                                    #
            slope_mod = (slope % stepval) ** -1  #
        
        #img.putpixel(start, color) #put first pixel at start
        count2 = 1
        while cursor[0] < end[0]: #REPEAT UNTIL THE CURSOR REACHES THE END       
            cursor[0] += 1
            
            #img.putpixel(cursor, color) # fill in the steps (optional: changes the line's style)
            
            count1 = stepval
            if slope != 0: #not horizontal line
                while count1 > 0:
                    cursor[1] += 1
                    img.putpixel(cursor, color)
                    count1 -= 1
                #END OF STEP
                count2 = (count2 + 1) % slope_mod
                    
                if count2 < 1: #add 1px if needed
                    cursor[1] += 1
                    img.putpixel(cursor, color)
            else:
                img.putpixel(cursor, color)
##########################################################################                    
    elif start[0] == end[0]: #vertical line
        cursor = list(start)
        v_steps = end[1] - start[1]
        
        v_count = 0
        if v_steps > 0:
            while v_count < v_steps:
                img.putpixel((cursor[0], start[1]+v_count), color)
                v_count += 1
                
