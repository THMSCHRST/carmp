import pygame
from perlin_noise import PerlinNoise
import random

# --- Config ---
WIDTH, HEIGHT = 800, 600
SCALE = 100  # Lower = zoomed in, higher = more spaced out
THRESHOLD = 0.01  # Higher = thinner clouds
OCTAVES = 4

# --- Init ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Perlin Noise Clouds ☁️")
clock = pygame.time.Clock()

# Create Perlin noise instance
noise = PerlinNoise(octaves=OCTAVES, seed=random.randint(0, 100))


def pixelate(surface, pixel_size):
    # Step 1: Scale down
    small = pygame.transform.scale(
        surface, (surface.get_width() // pixel_size, surface.get_height() // pixel_size)
    )

    # Step 2: Scale back up (with smooth off to keep it blocky)
    pixelated = pygame.transform.scale(small, surface.get_size())
    return pixelated


# --- Cloud Generation Function ---
def generate_clouds(offset_x=0, offset_y=0):
    surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    for y in range(HEIGHT):
        for x in range(WIDTH):
            nx = (x + offset_x) / SCALE
            ny = (y + offset_y) / SCALE
            value = noise([nx, ny])
            if value > THRESHOLD:
                alpha = int((value - THRESHOLD) / (1 - THRESHOLD) * 255)
                surface.set_at((x, y), (255, 255, 255, alpha))
    return surface


cloud_surface = pixelate(generate_clouds(), 10)

# --- Main Loop ---
offset_x = 0
offset_y = 0
running = True
while running:
    screen.fill((135, 206, 235))  # Sky blue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Animate clouds slowly
    # offset_x += 1

    screen.blit(cloud_surface, (0, 0))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
