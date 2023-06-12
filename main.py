from engine_functions import draw_line
from __init__ import render_res, upscale_res, root, lmain
from tkinter import *
from PIL import ImageTk, Image, ImageOps, ImageDraw, ImageFont
from itertools import product
import time
import numpy


def render_frame(frame):
    start = time.time_ns()
    
    #CREATE BLACK CANVAS (blanking interval)
    img = Image.new("RGB", size=(render_res, render_res), color=(0, 0, 0))

    #RENDER
    px_list = range(render_res)
    for x, y in product(px_list, px_list):
        color = (int(x*(255/render_res)), int(y*(255/render_res)), 255)
        img.putpixel((x, y), color)
        
    ##ANIMATE TEST POLYGON
    #bottom line moves up and down between 7 and 60
    #for some reason draw_line() doesn't like bottom-to-top lines
    speed = 1.0
    y_pos = int(((numpy.sin(numpy.deg2rad(frame*speed % 360)) + 1) / 2) * 53 + 7) #sorry, this is hard to read
    draw_line(img, (5, 5), [35, 5], (255, 255, 0))
    draw_line(img, (35, 5), [59, y_pos], (255, 255, 0))
    draw_line(img, (59, y_pos), [29, y_pos], (255, 255, 0))
    draw_line(img, (29, y_pos), [5, 5], (255, 255, 0))
    
    img.putpixel([5, 5], (0, 0, 0))
    img.putpixel([35, 5], (0, 0, 0))
    img.putpixel([59, y_pos], (0, 0, 0))
    img.putpixel([29, y_pos], (0, 0, 0))
    
    # VERTICAL LINE (bottom-to-top)
    # draw_line(img, (40, 55), [40, 5], (255, 255, 0))
    # # DIAGONAL
    # draw_line(img, (20, 10), [50, 60], (255, 255, 0))
    # img.putpixel([20, 10], (0, 0, 0))
    # img.putpixel([50, 60], (0, 0, 0))
            
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
