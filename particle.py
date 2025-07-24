import pygame
import random


class Particle:
    def __init__(self, name, x, y, scale, off, vscale, life=(60, 100), track=True):
        self.texture = pygame.transform.scale_by(
            pygame.image.load(rf"assets\{name}.png").convert_alpha(), scale
        )
        self.original_texture = self.texture.copy()
        self.x = x + off[0]
        self.y = y + off[1]

        self.vx = random.uniform(-1.5, 1.5) * vscale
        self.vy = random.uniform(-1.5, 1.5) * vscale
        self.track = track
        self.time = 0
        self.lifetime = random.randint(life[0], life[1])
        self.life = True

    def tick(self, screen, car):
        self.time += 1
        if self.time >= self.lifetime:
            self.life = False
            return

        self.x += self.vx
        self.y += self.vy

        alpha = max(0, 255 - int((self.time / self.lifetime) * 255))
        faded_texture = self.original_texture.copy()
        faded_texture.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MULT)

        if self.track:
            screen.blit(faded_texture, (self.x - car.x, self.y - car.y))
