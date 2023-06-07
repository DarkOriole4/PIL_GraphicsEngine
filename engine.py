from tkinter import *
from PIL import ImageTk, Image, ImageOps, ImageDraw, ImageFont
from itertools import product
import time
import numpy

render_res = 64
upscale_res = 862
refresh_time = 25 #ms

root = Tk()
# Create a frame
app = Frame(root, bg="white")
app.grid()
# Create a label in the frame
lmain = Label(app)
lmain.grid()



def draw_line(start, end, color):
    if start[0]<0 or start[1]<0 or start[0]>render_res or start[1]>render_res:
        raise ValueError('Invalid start coordinate')
    elif end[0]<0 or end[1]<0 or end[0]>render_res or end[1]>render_res:
        raise ValueError('Invalid end coordinate')
    
    
    #FIX DRAW DIRECTION
    if start[0] > end[0]: #if right-to-left, swap start with end
        temp = end
        end = start
        start = temp
    
    if start[1] > end[1]: #if bottom-to-top, swap top with bottom
        temp = end
        end = start
        start = temp
        
    
    elif start[0] != end[0]: #non-vertical line
        cursor = list(start)
        slope = numpy.abs(end[1] - start[1]) / numpy.abs(end[0] - start[0])
        stepval = int(slope) #slope's whole component
        if slope > 1 and slope < -1:             #
            slope_mod = (slope % stepval) ** -1  # slope_mod: the frequency at which an additional px needs to be added
        else:                                    #
            slope_mod = slope ** -1              #
        
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
                    
                if count2 < 0.05: #add 1px if needed
                    cursor[1] += 1
                    img.putpixel(cursor, color)
            else:
                img.putpixel(cursor, color)
                    
            
            
    elif start[0] == end[0]: #vertical line
        cursor = list(start)
        v_steps = end[1] - start[1]
        
        v_count = 0
        if v_steps > 0:
            while v_count < v_steps:
                img.putpixel((cursor[0], start[1]+v_count), color)
                v_count += 1
                
def render_frame(frame):
    global img
    start = time.time_ns()
    
    #CREATE BLACK CANVAS
    img = Image.new("RGB", size=(render_res, render_res), color=(0, 0, 0))
    
    #RENDER
    px_list = range(render_res)
    for x, y in product(px_list, px_list):
        color = (int(x*(255/render_res)), int(y*(255/render_res)), 255)
        img.putpixel((x, y), color)
        
    ##ANIMATE TEST POLYGON
    #bottom line moves up and down between 5 and 60
    #for some reason draw_line() doesn't like bottom-to-top lines
    y_pos = int(((numpy.sin(numpy.deg2rad(frame%360)) + 1) / 2) * 55 + 5) #sorry, this is hard to read
    draw_line((5, 5), [35, 5], (255, 255, 0))
    # draw_line((35, 5), [59, y_pos], (255, 255, 0))
    draw_line((59, y_pos), [29, y_pos], (255, 255, 0))
    # draw_line((29, y_pos), [5, 5], (255, 255, 0))
    
    img.putpixel([5, 5], (0, 0, 0))
    img.putpixel([35, 5], (0, 0, 0))
    img.putpixel([59, y_pos], (0, 0, 0))
    img.putpixel([29, y_pos], (0, 0, 0))
            
    #UPSCALE
    factor = upscale_res / render_res
    img = ImageOps.scale(img, factor, 4)

    #DRAW METADATA
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(r'C:/Users/Adrian/Downloads/Aileron-SemiBold.ttf', 15)
    end = time.time_ns()
    frame_time = (end-start)/1000000
    fps = 1000 / frame_time
    draw.text((5,5), 'frame_time: %dms\nfps: %d' % (frame_time, fps), fill=(255, 255, 255), font=font, spacing=5, align='left')
    #draw.text((5, upscale_res-20), 'frame: %d' % (frame), fill=(255, 255, 255), font=font)
    
    return img

# function for refreshing the screen
def refresh_screen():
    global frame
    imgtk = ImageTk.PhotoImage(image=render_frame(frame))
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    frame += 1
    lmain.after(1, refresh_screen) #wait for the refresh time



#MAIN
frame = 0
refresh_screen()
root.mainloop()
