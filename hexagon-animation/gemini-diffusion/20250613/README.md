# Output
```txt

Explanation:

Constants: Define screen dimensions, hexagon properties, ball properties, gravity, friction, bounce factor, initial ball count, and speed range.

Global Variables: Store the list of Ball objects, the current angular_speed, the Tkinter canvas and root windows, and the speed_scale widget.

get_hexagon_vertices(cx, cy, r): Calculates the coordinates of the six vertices of a hexagon centered at (cx, cy) with radius r.

rotate_point(point, center, angle): Rotates a given point around a center by a specified angle (in radians).

get_distance(p1, p2): Calculates the Euclidean distance between two points.

Ball Class:

__init__: Initializes a ball with position (x, y), velocity (vx, vy), color, and creates a corresponding oval object on the canvas.

update: Applies gravity to the vertical velocity (vy), applies friction to both velocities (vx, vy), updates the ball's position based on its velocity, and updates the canvas object's coordinates.

check_wall_collisions: Iterates through the edges of the hexagon. For each edge, it calculates the closest point on the line segment to the ball. If the distance is less than the ball's radius, a collision is detected. It then calculates the normal vector (from the closest point to the ball), reflects the ball's velocity off this normal, applies the BOUNCE_FACTOR, and slightly moves the ball back to prevent sticking.

check_ball_collisions: Iterates through all other balls. If the distance between two balls is less than the sum of their radii, a collision is detected. It calculates the normal vector (from the other ball to the current ball), the relative velocity, calculates an impulse (simplified, assuming equal mass), applies the impulse to both balls' velocities, and slightly moves the balls apart.

add_ball(): Creates a new Ball object at a random position within the hexagon's bounding box with a random initial velocity and adds it to the balls list.

update_speed(value): This function is called by the Tkinter slider when its value changes. It maps the slider's value (0-100) to the desired angular_speed range (MIN_ANGULAR_SPEED to MAX_ANGULAR_SPEED).

animate(): This is the main animation loop.

It gets the current hexagon vertices.

It rotates the vertices based on the current angular_speed.

It deletes the old hexagon drawing and creates a new one with the rotated vertices.

It iterates through all balls, calling their update, check_wall_collisions, and check_ball_collisions methods.

It uses root.after(30, animate) to schedule the animate function to run again after 30 milliseconds (approximately 30 frames per second).

setup_gui():

Creates the main Tkinter window (root) and the canvas.

Calls add_ball() multiple times to create the initial set of balls.

Creates a Frame to hold the control widgets (slider and button).

Creates a Scale (slider) for controlling the spin speed, linking it to the update_speed function. Sets the initial slider position based on the initial angular_speed.

Creates a Button for adding more balls, linking it to the add_ball function.

Calls animate() to start the animation loop.

Starts the Tkinter event loop (root.mainloop()).

if __name__ == "__main__":: Ensures that setup_gui() is called only when the script is executed directly.

To Run This Code:

Save it as a Python file (e.g., bouncing_hexagon.py).

Make sure you have Python installed.

Run it from your terminal: python bouncing_hexagon.py

You should see a window with a spinning hexagon and balls bouncing inside it. You can use the slider to change the hexagon's rotation speed and the "Add Ball" button to increase the number of balls.
```

# 速度
4069 tokens
/
4.665s
=
873 tokens/s