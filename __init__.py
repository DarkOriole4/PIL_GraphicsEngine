from tkinter import *
from PIL import Image

render_res = 256
upscale_res = 862
UPSCALE_RATIO = render_res / 64

## Window  Settings
root = Tk()
# Create a frame
app = Frame(root, bg="white")
app.grid()
root.resizable(False, False)
# Create a label in the frame
lmain = Label(app)
lmain.grid()