from engine_functions import draw_line, import_model, draw_wireframe, rotate_mesh
from __init__ import render_res, upscale_res, root, lmain
from tkinter import *
from PIL import ImageTk, Image, ImageOps, ImageDraw, ImageFont
from itertools import product
import time
import numpy
from math import radians


def render_frame(frame):
    start = time.time_ns()
    
    #CREATE BLANK CANVAS (blanking interval)
    img = Image.new("RGB", size=(render_res, render_res), color=(0, 100, 100))

    #RENDER
    # px_list = range(render_res)
    # for x, y in product(px_list, px_list):
    #     color = (int(x*(255/render_res)), int(y*(255/render_res)), 255)
    #     img.putpixel((x, y), color)
        
    # ##ANIMATE TEST POLYGON
    # top line is at y_pos 33
    # bottom line moves up and down between y_pos 7 and 60
    # speed = 2.0
    # y_pos = int(((numpy.sin(numpy.deg2rad(frame*speed % 360)) + 1) / 2) * 53 + 7) #sorry, this is hard to read
    # draw_line(img, (5, 33), [35, 33], (255, 255, 0))
    # draw_line(img, (35, 33), [59, y_pos], (255, 255, 0))
    # draw_line(img, (59, y_pos), [29, y_pos], (255, 255, 0))
    # draw_line(img, (29, y_pos), [5, 33], (255, 255, 0))

    ## DRAW WIREFRAME
    rotated_table = rotate_mesh(vertex_table, radians(frame))
    draw_wireframe(img, rotated_table, edge_table, (40, 255, 125))

    #UPSCALE
    factor = upscale_res / render_res
    img = ImageOps.scale(img, factor, 4)

    #DRAW METADATA
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(r'C:/Users/Adrian/Downloads/Aileron-SemiBold.ttf', 15)
    end = time.time_ns()
    frame_time = (end-start)/1000000
    fps = 1000 / frame_time
    draw.text((5,5), 'frame_time: %dms\nfps: %d' % (frame_time, fps), fill=(255, 255, 255), font=font, spacing=5, align='left') # displays frame time and fps
    #draw.text((5, upscale_res-20), 'frame: %d' % (frame), fill=(255, 255, 255), font=font) # displays frame count
    
    return img


def refresh_screen():
    global frame
    imgtk = ImageTk.PhotoImage(image=render_frame(frame))
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    frame += 1
    lmain.after(1, refresh_screen) #wait for the refresh time
    
    

if __name__ == "__main__":
    vertex_table, edge_table = import_model(__file__[:-7] + "primitives\Torus.txt")

    frame = 0
    refresh_screen()
    root.mainloop()