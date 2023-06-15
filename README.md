# PIL_GraphicsEngine
A 2D/3D graphics engine built entirely from scratch, using my very limited knowledge of raster rendering and the Python Image Library (PIL)

I don't usually use github, or make my code public but I want a way to easily manage my code and thought that maybe someone else could use it too.
So feel free to take it if you want, make it run faster or something - as long as you keep it open source I won't mind

<em>Please don't judge, I'm doing this for fun</em>

# How to use
1. Extract the repository
2. Install these dependencies (if you don't have them already):
   - `pip install numpy`
   - `pip install numba`
   - `pip install pillow`
3. Edit the `engine_cycle` function to display what you want *(optional)*
4. Run main.py

# Functionalities
At any given moment, whatever is displayed for every frame is dictated by the "engine_cycle" function that's located in main.py.

- You can change the color of any pixel on the screen using 
```
for x in range(render_res):
  for y in range(render_res):
    img.putpixel(x, y, color)
```
`render_res` is the resolution at which the screen is rendered. Later, it get's scaled up to the `upscale_res` and displayed.   

- You can animate things in code using the `frame` variable. It acts as an ever-incrementing clock counter


 ### There are a few functions that can be used to manipulate the engine:
- `draw_line(arr, start_coors, end_coors, color)` will draw a line given a startpoint, endpoint and color.  
At this moment in time lines don't have any thickness (they have a constant thickness of 1px).

**Important!** *in order for this function to run on the GPU, it requires the image to be an array for the input. Then it needs to be converted back to an image*

arr: *the img object converted to an array*

start_coors, end_coors: ``[x, y]`` - *a 2 element list or tuple with values that belong to the canvas*

color: ``[r, g, b]`` - *a 3 element list or tuple with 3 values between 0 and 255 that represent red, green and blue*

 **Example:** `draw_line(img, [256, 100], [123, 15], (255, 6, 181))`
 
---------------------------------------------------------
- `draw_wireframe(arr, vertex_table, edge_table, color)` will draw a 2D projection of a previously imported mesh as a wireframe.

**Important!** *in order for this function to run on the GPU, it requires the image to be an array for the input. Then it needs to be converted back to an image*

arr: *the img object converted to an array*

vertex_table: *a table that contains the coordinates of every vertex of a mesh*

edge_table: *a table that contains the coonnections between vertices for every edge of a mesh*

color: ``[r, g, b]`` - *a 3 element list or tuple with 3 values between 0 and 255 that represent red, green and blue*

**Example:** `img = draw_wireframe(arr, rotated_table, edge_table, (40, 255, 125))`

**Inside of the function, you can change a few key variables that control the shape of the viewing frustum:**

`fovy`: The angle between the upper and lower sides of the viewing frustum

`near`: Number Distance to the near clipping plane along the -Z axis

`far`: Number Distance to the far clipping plane along the -Z axis

<a href="https://www.researchgate.net/figure/A-viewing-frustum-defined-in-OpenGL-to-emulate-the-real-camera_fig1_261264621"><img src="https://docs.cocos2d-x.org/cocos2d-x/v4/en/3d/3d-img/PerspectiveCamera.png" alt="A viewing frustum defined to emulate the real camera"/></a>

---------------------------------------------------------
- `import_model(filepath)` will return both a vertex table and an edge table for any given file in the correct format.

filepath: *a path to a text file containing the data*

**Example:** `vertex_table, edge_table = import_model("primitives/Torus.txt")`

--------------------------------------------------------
- `rotate_mesh(vertex_table, angle)` given a vertex table, it returns another that is rotated on the vertical axis by a specified angle.

vertex_table: *a table that contains the coordinates of every vertex of a mesh*

angle: *an angle value in radians*

**Example:** `rotated_table = rotate_mesh(vertex_table, math.radians(60))`
