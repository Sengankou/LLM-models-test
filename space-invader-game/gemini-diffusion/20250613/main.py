import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Modern Space Invaders")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
LIGHT_BLUE = (100, 149, 237)
LIGHT_GREEN = (50, 205, 50)
LIGHT_RED = (255, 99, 71)

# Player settings
player_width = 50
player_height = 40
player_x = SCREEN_WIDTH // 2 - player_width // 2
player_y = SCREEN_HEIGHT - player_height - 20
player_speed = 8
player_color = CYAN

# Invader settings
invader_width = 40
invader_height = 30
invader_rows = 5
invader_cols = 8
invader_padding = 10
invader_speed_x = 3
invader_speed_y = 20
invader_colors = [RED, ORANGE, YELLOW, GREEN, MAGENTA]
invaders = []

# Bullet settings
bullet_width = 6
bullet_height = 20
bullet_speed = 10
bullet_color = YELLOW
bullets = []

# Invader bullet settings
invader_bullet_width = 4
invader_bullet_height = 15
invader_bullet_speed = 5
invader_bullet_color = LIGHT_RED
invader_bullets = []

# Game state
game_over = False
running = True
score = 0

# Font
try:
    font = pygame.font.Font(None, 48)  # Use default font
except pygame.error:
    # Fallback if default font is not available
    print("Warning: Default font not found. Using fallback font.")
    try:
        font = pygame.font.SysFont("Arial", 48)
    except pygame.error:
        print("Warning: Arial font not found. Using basic font.")
        font = None


def create_invaders():
    """Creates the grid of invaders."""
    global invaders
    invaders = []
    for row in range(invader_rows):
        for col in range(invader_cols):
            x = 50 + col * (invader_width + invader_padding)
            y = 50 + row * (invader_height + invader_padding)
            color = invader_colors[row % len(invader_colors)]
            invaders.append(
                {
                    "x": x,
                    "y": y,
                    "width": invader_width,
                    "height": invader_height,
                    "color": color,
                    "rect": pygame.Rect(x, y, invader_width, invader_height),
                }
            )


def draw_player():
    """Draws the player spaceship."""
    pygame.draw.rect(screen, player_color, (player_x, player_y, player_width, player_height))
    # Add a subtle glow effect
    pygame.draw.circle(screen, LIGHT_BLUE, (player_x + player_width // 2, player_y + player_height), player_width // 2, 2)


def draw_invaders():
    """Draws all invaders."""
    for invader in invaders:
        pygame.draw.rect(screen, invader["color"], invader["rect"])
        # Add a simple white outline
        pygame.draw.rect(screen, WHITE, invader["rect"], 1)
        # Add a small glowing circle for detail
        pygame.draw.circle(
            screen,
            LIGHT_GREEN,
            (invader["x"] + invader["width"] // 2, invader["y"] + invader["height"] // 2),
            invader["width"] // 4,
            1,
        )


def draw_bullets():
    """Draws player bullets."""
    for bullet in bullets:
        pygame.draw.rect(screen, bullet_color, (bullet["x"], bullet["y"], bullet_width, bullet_height))


def draw_invader_bullets():
    """Draws invader bullets."""
    for bullet in invader_bullets:
        pygame.draw.rect(screen, invader_bullet_color, (bullet["x"], bullet["y"], invader_bullet_width, invader_bullet_height))


def move_bullets():
    """Moves player bullets."""
    for bullet in bullets:
        bullet["y"] -= bullet_speed
        if bullet["y"] < 0:
            bullets.remove(bullet)


def move_invader_bullets():
    """Moves invader bullets."""
    for bullet in invader_bullets:
        bullet["y"] += invader_bullet_speed
        if bullet["y"] > SCREEN_HEIGHT:
            invader_bullets.remove(bullet)


def move_invaders():
    """Moves the invaders grid and checks for boundaries."""
    global invader_speed_x, invader_speed_y
    if not invaders:
        return

    # Check boundaries and reverse
    move_down = False
    for invader in invaders:
        invader["x"] += invader_speed_x
        invader["rect"].x = invader["x"]
        if invader["rect"].right >= SCREEN_WIDTH or invader["rect"].left <= 0:
            move_down = True

    if move_down:
        invader_speed_x *= -1
        for invader in invaders:
            invader["y"] += invader_speed_y
            invader["rect"].y = invader["y"]


def check_collisions():
    """Checks for collisions between bullets, invaders, and player."""
    global score, game_over, invaders

    # Player bullets vs Invaders
    bullets_to_remove = []
    invaders_to_remove = []
    for bullet in bullets:
        for invader in invaders:
            if invader["rect"].colliderect(bullet["rect"]):
                bullets_to_remove.append(bullet)
                invaders_to_remove.append(invader)
                score += 10
                break  # Bullet hits only one invader

    for bullet in bullets_to_remove:
        if bullet in bullets:
            bullets.remove(bullet)
    for invader in invaders_to_remove:
        if invader in invaders:
            invaders.remove(invader)

    # Invader bullets vs Player
    invader_bullets_to_remove = []
    for bullet in invader_bullets:
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        if player_rect.colliderect(bullet["rect"]):
            invader_bullets_to_remove.append(bullet)
            game_over = True
            break

    for bullet in invader_bullets_to_remove:
        if bullet in invader_bullets:
            invader_bullets.remove(bullet)

    # Check if invaders reached the bottom
    for invader in invaders:
        if invader["rect"].bottom >= player_y:
            game_over = True
            break


def invader_shoot():
    """Randomly makes an invader shoot a bullet."""
    global invader_bullets
    if not invaders:
        return

    if random.random() < 0.01:  # 1% chance per frame (adjustable)
        shooter_invader = random.choice(invaders)
        invader_bullets.append(
            {
                "x": shooter_invader["x"] + shooter_invader["width"] // 2 - invader_bullet_width // 2,
                "y": shooter_invader["y"] + shooter_invader["height"],
                "width": invader_bullet_width,
                "height": invader_bullet_height,
                "rect": pygame.Rect(
                    shooter_invader["x"] + shooter_invader["width"] // 2 - invader_bullet_width // 2,
                    shooter_invader["y"] + shooter_invader["height"],
                    invader_bullet_width,
                    invader_bullet_height,
                ),
            }
        )


def display_score():
    """Displays the current score."""
    if font:
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))


def display_game_over_text():
    """Displays the game over message."""
    if font:
        game_over_text = font.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(game_over_text, game_over_rect)

        score_text = font.render(f"Final Score: {score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        screen.blit(score_text, score_rect)

        restart_text = font.render("Press R to Restart", True, YELLOW)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        screen.blit(restart_text, restart_rect)


# Game loop
create_invaders()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bullets.append(
                    {
                        "x": player_x + player_width // 2 - bullet_width // 2,
                        "y": player_y,
                        "width": bullet_width,
                        "height": bullet_height,
                        "rect": pygame.Rect(
                            player_x + player_width // 2 - bullet_width // 2, player_y, bullet_width, bullet_height
                        ),
                    }
                )
            if event.key == pygame.K_r and game_over:
                game_over = False
                score = 0
                bullets = []
                invader_bullets = []
                create_invaders()
                player_x = SCREEN_WIDTH // 2 - player_width // 2

    if not game_over:
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
            player_x += player_speed

        # Move bullets
        move_bullets()
        move_invader_bullets()

        # Move invaders
        move_invaders()

        # Invader shooting
        invader_shoot()

        # Check collisions
        check_collisions()

    # Clear the screen
    screen.fill(BLACK)  # Use a dark background

    # Draw game elements
    draw_player()
    draw_invaders()
    draw_bullets()
    draw_invader_bullets()
    display_score()

    if game_over:
        display_game_over_text()

    # Update the display
    pygame.display.flip()

    # Control frame rate
    pygame.time.Clock().tick(60)  # 60 frames per second

# Quit Pygame
pygame.quit()
