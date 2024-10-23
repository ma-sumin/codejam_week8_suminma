import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH, HEIGHT = 800, 800
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Satellite Orbit Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Load images
background_img = pygame.image.load('space_background.png')
earth_img = pygame.image.load('earth.png')
satellite_img = pygame.image.load('satellite.webp')
debris_img = pygame.image.load('debris.png')

# Resize images
earth_img = pygame.transform.scale(earth_img, (180, 180))  # Earth image size
satellite_img = pygame.transform.scale(satellite_img, (30, 30))  # Satellite size
debris_img = pygame.transform.scale(debris_img, (20, 20))  # Debris size

# Earth and satellite parameters
EARTH_RADIUS = 100
SATELLITE_RADIUS = 10
EARTH_POS = (WIDTH // 2, HEIGHT // 2)
MAX_ALTITUDE = 300

# Satellite parameters
satellite_angle = 0  # Position of satellite in orbit (in degrees)
satellite_velocity = 0.8  # Slower speed for satellite
satellite_altitude = 150  # Distance from the center of the Earth
satellite_direction = 1  # Clockwise or counterclockwise

# Debris parameters
debris_list = []
DEBRIS_RADIUS = 5

# Font for text
font = pygame.font.SysFont('Arial', 30)

# Game state
game_started = False
game_over = False

def draw_intro():
    """Draw the introduction screen."""
    win.fill(BLACK)
    title = font.render("Welcome to the Satellite Orbit Game!", True, WHITE)
    instructions = font.render("Press SPACE to start", True, WHITE)
    controls = font.render("Use arrow keys to control satellite.", True, WHITE)
    win.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 100))
    win.blit(instructions, (WIDTH // 2 - instructions.get_width() // 2, HEIGHT // 2 - 50))
    win.blit(controls, (WIDTH // 2 - controls.get_width() // 2, HEIGHT // 2))
    pygame.display.update()

def draw_earth():
    """Draw the Earth."""
    win.blit(earth_img, (EARTH_POS[0] - EARTH_RADIUS, EARTH_POS[1] - EARTH_RADIUS))

def draw_satellite():
    """Draw the satellite in orbit."""
    global satellite_angle
    satellite_angle += satellite_velocity * satellite_direction
    if satellite_angle >= 360:
        satellite_angle = 0

    # Calculate satellite position based on angle and altitude
    satellite_x = EARTH_POS[0] + satellite_altitude * math.cos(math.radians(satellite_angle))
    satellite_y = EARTH_POS[1] + satellite_altitude * math.sin(math.radians(satellite_angle))

    win.blit(satellite_img, (int(satellite_x) - SATELLITE_RADIUS, int(satellite_y) - SATELLITE_RADIUS))
    return (satellite_x, satellite_y)

def generate_debris():
    """Generate random debris in orbit."""
    angle = random.randint(0, 360)
    altitude = random.randint(EARTH_RADIUS + 50, MAX_ALTITUDE)
    x = EARTH_POS[0] + altitude * math.cos(math.radians(angle))
    y = EARTH_POS[1] + altitude * math.sin(math.radians(angle))
    return [x, y]

def draw_debris():
    """Draw space debris in orbit."""
    for debris in debris_list:
        win.blit(debris_img, (int(debris[0]) - DEBRIS_RADIUS, int(debris[1]) - DEBRIS_RADIUS))

def detect_collision(satellite_pos):
    """Check if the satellite has collided with any debris."""
    for debris in debris_list:
        distance = math.sqrt((satellite_pos[0] - debris[0]) ** 2 + (satellite_pos[1] - debris[1]) ** 2)
        if distance <= SATELLITE_RADIUS + DEBRIS_RADIUS:
            return True
    return False

def display_info():
    """Display the satellite's altitude and velocity on the screen."""
    altitude_text = font.render(f'Altitude: {satellite_altitude} km', True, WHITE)
    velocity_text = font.render(f'Velocity: {satellite_velocity:.2f} km/s', True, WHITE)
    win.blit(altitude_text, (10, 10))
    win.blit(velocity_text, (10, 50))

# Main game loop
run = True
clock = pygame.time.Clock()

while run:
    clock.tick(60)
    
    if not game_started:
        draw_intro()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_started = True
        continue
    
    if game_over:
        win.fill(BLACK)
        game_over_text = font.render("Game Over! Press ESC to quit.", True, RED)
        win.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                run = False
        continue

    win.blit(background_img, (0, 0))  # Draw space background

    # Draw Earth and satellite
    draw_earth()
    satellite_pos = draw_satellite()

    # Display altitude and velocity
    display_info()

    # Generate random debris every few frames
    if random.randint(1, 50) == 1:
        debris_list.append(generate_debris())

    # Draw debris and check for collisions
    draw_debris()
    if detect_collision(satellite_pos):
        game_over = True

    # Handle player input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and satellite_altitude > EARTH_RADIUS + 50:
        satellite_altitude -= 1
    if keys[pygame.K_DOWN] and satellite_altitude < MAX_ALTITUDE:
        satellite_altitude += 1
    if keys[pygame.K_LEFT]:
        satellite_velocity = max(0.1, satellite_velocity - 0.01)  # Limit to not go below 0.1
    if keys[pygame.K_RIGHT]:
        satellite_velocity += 0.01

    # Close the game window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()