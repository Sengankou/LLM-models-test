import pygame
import math
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
GRAVITY = 0.3
FRICTION = 0.98
BOUNCE_DAMPING = 0.8

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)

BALL_COLORS = [RED, BLUE, GREEN, YELLOW, PURPLE, ORANGE, CYAN]


class Ball:
    def __init__(self, x, y, radius=15):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.radius = radius
        self.color = random.choice(BALL_COLORS)
        self.mass = radius / 10.0

    def update(self):
        # Apply gravity
        self.vy += GRAVITY

        # Apply friction
        self.vx *= FRICTION
        self.vy *= FRICTION

        # Update position
        self.x += self.vx
        self.y += self.vy

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), self.radius, 2)


class Hexagon:
    def __init__(self, center_x, center_y, radius):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.angle = 0
        self.rotation_speed = 0

    def update(self):
        self.angle += self.rotation_speed

    def get_vertices(self):
        vertices = []
        for i in range(6):
            angle = self.angle + i * math.pi / 3
            x = self.center_x + self.radius * math.cos(angle)
            y = self.center_y + self.radius * math.sin(angle)
            vertices.append((x, y))
        return vertices

    def get_edges(self):
        vertices = self.get_vertices()
        edges = []
        for i in range(6):
            start = vertices[i]
            end = vertices[(i + 1) % 6]
            edges.append((start, end))
        return edges

    def draw(self, screen):
        vertices = self.get_vertices()
        pygame.draw.polygon(screen, LIGHT_GRAY, vertices, 3)


def point_to_line_distance(px, py, x1, y1, x2, y2):
    """Calculate the shortest distance from a point to a line segment"""
    A = px - x1
    B = py - y1
    C = x2 - x1
    D = y2 - y1

    dot = A * C + B * D
    len_sq = C * C + D * D

    if len_sq == 0:
        return math.sqrt(A * A + B * B)

    param = dot / len_sq

    if param < 0:
        xx = x1
        yy = y1
    elif param > 1:
        xx = x2
        yy = y2
    else:
        xx = x1 + param * C
        yy = y1 + param * D

    dx = px - xx
    dy = py - yy
    return math.sqrt(dx * dx + dy * dy), xx, yy


def check_ball_wall_collision(ball, hexagon):
    """Check and resolve collision between ball and hexagon walls"""
    edges = hexagon.get_edges()

    for edge in edges:
        (x1, y1), (x2, y2) = edge
        distance, closest_x, closest_y = point_to_line_distance(ball.x, ball.y, x1, y1, x2, y2)

        if distance < ball.radius:
            # Calculate normal vector
            dx = ball.x - closest_x
            dy = ball.y - closest_y
            length = math.sqrt(dx * dx + dy * dy)

            if length > 0:
                # Normalize
                nx = dx / length
                ny = dy / length

                # Move ball out of wall
                overlap = ball.radius - distance
                ball.x += nx * overlap
                ball.y += ny * overlap

                # Reflect velocity
                dot = ball.vx * nx + ball.vy * ny
                ball.vx -= 2 * dot * nx
                ball.vy -= 2 * dot * ny

                # Apply damping
                ball.vx *= BOUNCE_DAMPING
                ball.vy *= BOUNCE_DAMPING


def check_ball_ball_collision(ball1, ball2):
    """Check and resolve collision between two balls"""
    dx = ball2.x - ball1.x
    dy = ball2.y - ball1.y
    distance = math.sqrt(dx * dx + dy * dy)

    if distance < ball1.radius + ball2.radius and distance > 0:
        # Normalize collision vector
        nx = dx / distance
        ny = dy / distance

        # Separate balls
        overlap = ball1.radius + ball2.radius - distance
        ball1.x -= nx * overlap * 0.5
        ball1.y -= ny * overlap * 0.5
        ball2.x += nx * overlap * 0.5
        ball2.y += ny * overlap * 0.5

        # Calculate relative velocity
        dvx = ball2.vx - ball1.vx
        dvy = ball2.vy - ball1.vy

        # Calculate relative velocity along collision normal
        dvn = dvx * nx + dvy * ny

        # Do not resolve if velocities are separating
        if dvn > 0:
            return

        # Calculate collision impulse
        impulse = 2 * dvn / (ball1.mass + ball2.mass)

        # Update velocities
        ball1.vx += impulse * ball2.mass * nx
        ball1.vy += impulse * ball2.mass * ny
        ball2.vx -= impulse * ball1.mass * nx
        ball2.vy -= impulse * ball1.mass * ny


class Button:
    def __init__(self, x, y, width, height, text, color=LIGHT_GRAY):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.font = pygame.font.Font(None, 24)
        self.clicked = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)

        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, initial_val):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.val = initial_val
        self.dragging = False
        self.font = pygame.font.Font(None, 20)

    def draw(self, screen):
        # Draw slider track
        pygame.draw.rect(screen, GRAY, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)

        # Draw slider handle
        handle_x = self.rect.x + (self.val - self.min_val) / (self.max_val - self.min_val) * self.rect.width
        handle_rect = pygame.Rect(handle_x - 5, self.rect.y - 5, 10, self.rect.height + 10)
        pygame.draw.rect(screen, WHITE, handle_rect)
        pygame.draw.rect(screen, BLACK, handle_rect, 2)

        # Draw value text
        text = f"Speed: {self.val:.2f}"
        text_surface = self.font.render(text, True, BLACK)
        screen.blit(text_surface, (self.rect.x, self.rect.y - 25))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mouse_x = event.pos[0]
            relative_x = mouse_x - self.rect.x
            relative_x = max(0, min(relative_x, self.rect.width))
            self.val = self.min_val + (relative_x / self.rect.width) * (self.max_val - self.min_val)


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Bouncing Balls in Rotating Hexagon")
    clock = pygame.time.Clock()

    # Create hexagon
    hexagon = Hexagon(WIDTH // 2, HEIGHT // 2, 200)

    # Create initial balls
    balls = []
    for _ in range(5):
        x = WIDTH // 2 + random.uniform(-50, 50)
        y = HEIGHT // 2 + random.uniform(-50, 50)
        balls.append(Ball(x, y))

    # Create UI elements
    add_ball_button = Button(20, 20, 100, 40, "Add Ball")
    speed_slider = Slider(20, 80, 200, 20, -0.05, 0.05, 0)

    font = pygame.font.Font(None, 36)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if add_ball_button.is_clicked(event.pos):
                    # Add new ball at random position near center
                    x = WIDTH // 2 + random.uniform(-100, 100)
                    y = HEIGHT // 2 + random.uniform(-100, 100)
                    balls.append(Ball(x, y))

            speed_slider.handle_event(event)

        # Update hexagon rotation
        hexagon.rotation_speed = speed_slider.val
        hexagon.update()

        # Update balls
        for ball in balls:
            ball.update()

        # Check collisions
        for ball in balls:
            check_ball_wall_collision(ball, hexagon)

        # Check ball-ball collisions
        for i in range(len(balls)):
            for j in range(i + 1, len(balls)):
                check_ball_ball_collision(balls[i], balls[j])

        # Draw everything
        screen.fill(WHITE)

        # Draw hexagon
        hexagon.draw(screen)

        # Draw balls
        for ball in balls:
            ball.draw(screen)

        # Draw UI
        add_ball_button.draw(screen)
        speed_slider.draw(screen)

        # Draw ball count
        ball_count_text = font.render(f"Balls: {len(balls)}", True, BLACK)
        screen.blit(ball_count_text, (WIDTH - 150, 20))

        # Draw instructions
        instructions = [
            "Click 'Add Ball' to add more balls",
            "Use slider to control hexagon rotation",
            "Watch balls bounce and collide!",
        ]

        small_font = pygame.font.Font(None, 20)
        for i, instruction in enumerate(instructions):
            text = small_font.render(instruction, True, BLACK)
            screen.blit(text, (20, HEIGHT - 80 + i * 20))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
