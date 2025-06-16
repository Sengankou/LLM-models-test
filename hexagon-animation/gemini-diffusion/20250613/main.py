import tkinter as tk
import math
import random

# --- Constants ---
WIDTH = 800
HEIGHT = 600
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2
HEX_RADIUS = 200
BALL_RADIUS = 10
GRAVITY = 0.5
FRICTION = 0.98  # Reduces velocity slightly each frame
BOUNCE_FACTOR = 0.8  # How much velocity remains after bounce
INITIAL_BALLS = 5
INITIAL_ANGULAR_SPEED = 0.02  # radians per frame
MAX_ANGULAR_SPEED = 0.05  # radians per frame
MIN_ANGULAR_SPEED = 0.00  # radians per frame

# --- Global Variables ---
balls = []
angular_speed = INITIAL_ANGULAR_SPEED
canvas = None
root = None
speed_scale = None

# --- Helper Functions ---


def get_hexagon_vertices(cx, cy, r):
    """Calculates the vertices of a hexagon centered at cx, cy."""
    vertices = []
    for i in range(6):
        angle = math.pi / 6 + i * 2 * math.pi / 6
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        vertices.append((x, y))
    return vertices


def rotate_point(point, center, angle):
    """Rotates a point around a center by a given angle."""
    px, py = point
    cx, cy = center
    dx = px - cx
    dy = py - cy
    new_dx = dx * math.cos(angle) - dy * math.sin(angle)
    new_dy = dx * math.sin(angle) + dy * math.cos(angle)
    return (cx + new_dx, cy + new_dy)


def get_distance(p1, p2):
    """Calculates the distance between two points."""
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


# --- Ball Class ---


class Ball:
    def __init__(self, x, y, vx, vy, color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.id = canvas.create_oval(
            x - BALL_RADIUS, y - BALL_RADIUS, x + BALL_RADIUS, y + BALL_RADIUS, fill=color, outline="black"
        )

    def update(self):
        """Updates the ball's position and velocity."""
        # Apply gravity
        self.vy += GRAVITY

        # Apply friction
        self.vx *= FRICTION
        self.vy *= FRICTION

        # Update position
        self.x += self.vx
        self.y += self.vy

        # Update canvas object
        canvas.coords(self.id, self.x - BALL_RADIUS, self.y - BALL_RADIUS, self.x + BALL_RADIUS, self.y + BALL_RADIUS)

    def check_wall_collisions(self, hex_vertices):
        """Checks for collisions with the hexagon walls."""
        for i in range(len(hex_vertices)):
            p1 = hex_vertices[i]
            p2 = hex_vertices[(i + 1) % len(hex_vertices)]

            # Vector from p1 to p2
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]

            # Vector from p1 to ball
            ball_dx = self.x - p1[0]
            ball_dy = self.y - p1[1]

            # Project vector from p1 to ball onto vector from p1 to p2
            dot_product = ball_dx * dx + ball_dy * dy
            length_sq = dx * dx + dy * dy

            if length_sq == 0:  # p1 and p2 are the same point
                t = 0
            else:
                t = dot_product / length_sq

            t = max(0, min(1, t))  # Clamp t to [0, 1]

            # Closest point on the line segment to the ball
            closest_x = p1[0] + t * dx
            closest_y = p1[1] + t * dy

            # Distance from ball to closest point
            dist = get_distance((self.x, self.y), (closest_x, closest_y))

            if dist < BALL_RADIUS:
                # Collision detected!
                # Calculate normal vector (from closest point to ball)
                normal_x = self.x - closest_x
                normal_y = self.y - closest_y
                normal_length = math.sqrt(normal_x**2 + normal_y**2)

                if normal_length > 0:
                    normal_x /= normal_length
                    normal_y /= normal_length
                else:
                    # If normal_length is 0, it means ball is exactly on a vertex
                    # Use the vector from p1 to ball as normal
                    normal_x = self.x - p1[0]
                    normal_y = self.y - p1[1]
                    normal_length = math.sqrt(normal_x**2 + normal_y**2)
                    if normal_length > 0:
                        normal_x /= normal_length
                        normal_y /= normal_length
                    else:
                        # If still 0, use a random normal (unlikely)
                        normal_x = random.choice([-1, 1])
                        normal_y = random.choice([-1, 1])
                        normal_length = math.sqrt(normal_x**2 + normal_y**2)
                        if normal_length > 0:
                            normal_x /= normal_length
                            normal_y /= normal_length

                # Reflect velocity off the normal
                dot_product = self.vx * normal_x + self.vy * normal_y
                self.vx = self.vx - 2 * dot_product * normal_x
                self.vy = self.vy - 2 * dot_product * normal_y

                # Apply bounce factor
                self.vx *= BOUNCE_FACTOR
                self.vy *= BOUNCE_FACTOR

                # Move ball slightly back to prevent sticking
                overlap = BALL_RADIUS - dist
                self.x += normal_x * overlap
                self.y += normal_y * overlap
                canvas.coords(self.id, self.x - BALL_RADIUS, self.y - BALL_RADIUS, self.x + BALL_RADIUS, self.y + BALL_RADIUS)
                return True  # Collision occurred
        return False

    def check_ball_collisions(self, other_balls):
        """Checks for collisions with other balls."""
        for other_ball in other_balls:
            if self is other_ball:
                continue

            dist = get_distance((self.x, self.y), (other_ball.x, other_ball.y))
            if dist < 2 * BALL_RADIUS:
                # Collision detected!
                # Calculate normal vector (from other ball to self)
                normal_x = self.x - other_ball.x
                normal_y = self.y - other_ball.y
                normal_length = math.sqrt(normal_x**2 + normal_y**2)

                if normal_length > 0:
                    normal_x /= normal_length
                    normal_y /= normal_length
                else:
                    # If normal_length is 0, use a random normal
                    normal_x = random.choice([-1, 1])
                    normal_y = random.choice([-1, 1])
                    normal_length = math.sqrt(normal_x**2 + normal_y**2)
                    if normal_length > 0:
                        normal_x /= normal_length
                        normal_y /= normal_length

                # Calculate relative velocity
                rel_vx = self.vx - other_ball.vx
                rel_vy = self.vy - other_ball.vy

                # Project relative velocity onto normal
                dot_product = rel_vx * normal_x + rel_vy * normal_y

                if dot_product < 0:  # Only react if moving towards each other
                    # Calculate impulse (simplified, assuming equal mass)
                    impulse = -(1 + BOUNCE_FACTOR) * dot_product
                    impulse_x = impulse * normal_x
                    impulse_y = impulse * normal_y

                    # Apply impulse to velocities
                    self.vx += impulse_x
                    self.vy += impulse_y
                    other_ball.vx -= impulse_x
                    other_ball.vy -= impulse_y

                    # Move balls slightly apart to prevent sticking
                    overlap = 2 * BALL_RADIUS - dist
                    self.x += normal_x * overlap / 2
                    self.y += normal_y * overlap / 2
                    other_ball.x -= normal_x * overlap / 2
                    other_ball.y -= normal_y * overlap / 2

                    canvas.coords(
                        self.id, self.x - BALL_RADIUS, self.y - BALL_RADIUS, self.x + BALL_RADIUS, self.y + BALL_RADIUS
                    )
                    canvas.coords(
                        other_ball.id,
                        other_ball.x - BALL_RADIUS,
                        other_ball.y - BALL_RADIUS,
                        other_ball.x + BALL_RADIUS,
                        other_ball.y + BALL_RADIUS,
                    )
                    return True  # Collision occurred
        return False


# --- Game Logic ---


def add_ball():
    """Adds a new ball at a random position inside the hexagon."""
    x = random.uniform(CENTER_X - HEX_RADIUS * 0.8, CENTER_X + HEX_RADIUS * 0.8)
    y = random.uniform(CENTER_Y - HEX_RADIUS * 0.8, CENTER_Y + HEX_RADIUS * 0.8)
    vx = random.uniform(-2, 2)
    vy = random.uniform(-2, 2)
    color = random.choice(["red", "green", "blue", "yellow", "purple", "orange"])
    balls.append(Ball(x, y, vx, vy, color))


def update_speed(value):
    """Updates the angular speed based on the slider value."""
    global angular_speed
    angular_speed = MIN_ANGULAR_SPEED + (MAX_ANGULAR_SPEED - MIN_ANGULAR_SPEED) * (float(value) / 100.0)


def animate():
    """Main animation function."""
    global angular_speed

    # Get current hexagon vertices
    hex_vertices = get_hexagon_vertices(CENTER_X, CENTER_Y, HEX_RADIUS)

    # Rotate hexagon vertices
    rotated_vertices = [rotate_point(v, (CENTER_X, CENTER_Y), angular_speed) for v in hex_vertices]

    # Update hexagon drawing
    canvas.delete("hexagon")
    canvas.create_polygon(rotated_vertices, outline="black", fill="lightgray", width=2, tags="hexagon")

    # Update balls and check collisions
    for ball in balls:
        ball.update()
        ball.check_wall_collisions(rotated_vertices)
        ball.check_ball_collisions(balls)

    # Schedule next frame
    root.after(30, animate)  # Run approximately 30 times per second


# --- GUI Setup ---


def setup_gui():
    global root, canvas, speed_scale

    root = tk.Tk()
    root.title("Bouncing Balls in Spinning Hexagon")

    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
    canvas.pack()

    # Add initial balls
    for _ in range(INITIAL_BALLS):
        add_ball()

    # Create control frame
    control_frame = tk.Frame(root)
    control_frame.pack(pady=10)

    # Speed slider
    speed_label = tk.Label(control_frame, text="Spin Speed:")
    speed_label.pack(side=tk.LEFT, padx=5)
    speed_scale = tk.Scale(control_frame, from_=0, to=100, orient=tk.HORIZONTAL, length=200, command=update_speed)
    speed_scale.set((angular_speed - MIN_ANGULAR_SPEED) / (MAX_ANGULAR_SPEED - MIN_ANGULAR_SPEED) * 100)
    speed_scale.pack(side=tk.LEFT, padx=5)

    # Add ball button
    add_ball_button = tk.Button(control_frame, text="Add Ball", command=add_ball)
    add_ball_button.pack(side=tk.LEFT, padx=20)

    # Start animation
    animate()

    root.mainloop()


# --- Main Execution ---

if __name__ == "__main__":
    setup_gui()
