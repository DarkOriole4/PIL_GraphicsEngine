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
    
    elif start[0] != end[0]: #non-vertical line
        cursor = list(start)
        h_steps = numpy.abs(end[0] - start[0])
        v_steps = end[1] - start[1]
        slope = v_steps / h_steps
        
        h_count = 0
        v_count = 0
        while h_count < h_steps and h_count > -h_steps:
            img.putpixel(cursor, color)
            if start[0] < end[0]: #left to right
                h_count += 1
            else: #right to left
                h_count -= 1
            
            if numpy.abs(slope) > 1: #line requires unusual stepping
                subv_count = 0
                if slope >= 0:
                    while subv_count < int(slope):
                        subv_count += 1
                        img.putpixel((start[0]+h_count, start[1]+v_count+subv_count), color)
                else:
                    while subv_count > int(slope):
                        subv_count -= 1
                        img.putpixel((start[0]+h_count, start[1]+v_count+subv_count), color)
                        
            v_count += int(slope)
            cursor = [start[0]+h_count, start[1]+v_count] #increment cursor
            
    elif start[0] == end[0]: #vertical line
        cursor = list(start)
        h_steps = numpy.abs(end[0] - start[0])
        v_steps = end[1] - start[1]
        
        v_count = 0
        if v_steps > 0: # top to bottom
            while v_count < v_steps:
                img.putpixel((cursor[0], start[1]+v_count), color)
                v_count += 1 #top to bottom
                
        elif v_steps < 0: # bottom to top
            while v_count > v_steps:
                img.putpixel((cursor[0], start[1]+v_count), color)
                v_count -= 1

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
        
    # #draw test rowneglobok
    # draw_line((5, 5), (35, 5), (255, 255, 0))
    draw_line((35, 5), (59, 59), (255, 255, 0))
    # draw_line((59, 59), (29, 59), (255, 255, 0))
    # draw_line((29, 59), (5, 5), (255, 255, 0))
    
    # #DEBUG VERTICES
    # img.putpixel((5, 5), (0, 0, 0))
    # img.putpixel((35, 5), (0, 0, 0))
    # img.putpixel((59, 59), (0, 0, 0))
    # img.putpixel((29, 59), (0, 0, 0))
    
    # #draw test kwadrat
    # draw_line((5, 5), (35, 5), (255, 255, 0))
    # draw_line((35, 5), (35, 35), (255, 0, 255))
    # draw_line((35, 35), (5, 35), (0, 255, 255))
    # draw_line((5, 35), (5, 5), (255, 255, 255))
    
    # #DEBUG VERTICES
    # img.putpixel((5, 5), (0, 0, 0))
    # img.putpixel((35, 5), (0, 0, 0))
    # img.putpixel((35, 35), (0, 0, 0))
    # img.putpixel((5, 35), (0, 0, 0))
            
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
