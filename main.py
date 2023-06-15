from engine_functions import draw_frame, draw_line, import_model, draw_wireframe, rotate_mesh, convert_img2arr
from __init__ import render_res, upscale_res, root, lmain
from tkinter import *
from PIL import ImageTk, Image, ImageOps, ImageDraw, ImageFont
from itertools import product
import time
import numpy
from math import radians


def engine_cycle(frame):
    start = time.time_ns()
    
    # CREATE BLANK CANVAS (blanking interval)
    img = Image.new("RGB", size=(render_res, render_res), color=(0, 100, 100))

    # FILL IN BACKGROUND
    arr = convert_img2arr(img) # prepare for the GPU
    arr = draw_frame(arr)
    img = Image.fromarray(arr) # back to the CPU

    ## DRAW WIREFRAME
    rotated_table = rotate_mesh(vertex_table, radians(frame))

    arr = convert_img2arr(img)  # prepare for the GPU
    img = draw_wireframe(arr, rotated_table, edge_table, (40, 255, 125))

    #UPSCALE
    factor = upscale_res / render_res
    img = ImageOps.scale(img, factor, 4)

    #DRAW METADATA
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(r'C:/Users/Adrian/Downloads/Aileron-SemiBold.ttf', 15)
    end = time.time_ns()
    frame_time = (end-start)/1000000
    fps = 1000 / frame_time
    draw.text((5, 5), 'frame_time: %dms\nfps: %d' % (frame_time, fps), fill=(255, 255, 255), font=font, spacing=5, align='left') # displays frame time and fps
    #draw.text((5, upscale_res-20), 'frame: %d' % (frame), fill=(255, 255, 255), font=font) # displays frame count
    
    return img


def refresh_screen():
    global frame
    imgtk = ImageTk.PhotoImage(image=engine_cycle(frame))
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    frame += 1
    lmain.after(1, refresh_screen) #wait for the refresh time
    
    

if __name__ == "__main__":
    vertex_table, edge_table = import_model(__file__[:-7] + "primitives\Torus.txt")

    frame = 0
    refresh_screen()
    root.mainloop()