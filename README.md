# PIL_GraphicsEngine
A 2D/3D graphics engine built entirely from scratch, using my very limited knowledge of raster rendering and the Python Image Library (PIL)

I don't usually use github, or make my code public but I want a way to easily manage my code and thought that maybe someone else could use it too.
So feel free to take it if you want, make it run faster or something - as long as you keep it open source I won't mind

<em>Please don't judge, I'm doing this for fun</em>

# How to use
1. Extract the repository
2. Run main.py

# Functionalities
At any given moment, whatever is on the screen is decided by the "render_frame" function that's located in main.py.

- You can change the color of any pixel on the screen using 
```
for x in range(render_res):
  for y in range(render_res):
    img.putpixel(x, y, color)
```
`render_res` is the resolution at which the screen is rendered. Later, it get's scaled up to the `upscale_res` and displayed.  

---------------------------------------------------------
- `draw_line(img, start_coors, end_coors, color)` will draw a line given a startpoint, endpoint and color.  
At this moment in time lines don't have any thickness (they have a constant thickness of 1px).  

start_coors, end_coors: ``[x, y]`` - *a 2 element list or tuple with values that belong to the canvas*

color: ``[r, g, b]`` - *a 3 element list or tuple with 3 values between 0 and 255 that represent red, green and blue*

 **Example:** `draw_line(img, [256, 100], [123, 15], (255, 6, 181))`
 
---------------------------------------------------------
- `draw_wireframe(img, vertex_table, edge_table, color)` will draw a 2D projection of a previously imported mesh as a wireframe.

vertex_table: *a table that contains the coordinates of every vertex of a mesh*

edge_table: *a table that contains the coonnections between vertices for every edge of a mesh*

color: ``[r, g, b]`` - *a 3 element list or tuple with 3 values between 0 and 255 that represent red, green and blue*

**Example:** `draw_wireframe(img, vertex_table, edge_table, (255, 255, 255))`
