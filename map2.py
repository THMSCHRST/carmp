import pygame


class Map:
    def __init__(self, index, car):
        self.start = (0, 255, 255)
        self.end = (255, 255, 255)
        self.rendpos = (0, 0)
        self.rstartpos = (0, 0)
        self.scaled = False
        with open(rf"levels\{index}\options.txt", "r") as file:
            self.scale = float(file.read())
        self.hitbox = pygame.image.load(rf"levels\{index}\hitbox.png").convert_alpha()
        # self.overlay = pygame.image.load(rf"levels\{index}\map.png").convert_alpha()

    def scalef(self, car):
        self.scaled_hitbox = pygame.transform.scale_by(
            self.hitbox, self.scale
        ).convert_alpha()
        self.scaled_rect = self.scaled_hitbox.get_rect()
        image = self.hitbox
        found = False
        for y in range(image.get_height()):
            for x in range(image.get_width()):
                pixel_color = image.get_at((x, y))[:3]
                if pixel_color == self.end:
                    self.endpos = (float(x), float(y))
                    found = True
                    break
            if found:
                break
        found = False
        for y in range(image.get_height()):
            for x in range(image.get_width()):
                pixel_color = image.get_at((x, y))[:3]
                if pixel_color == self.start:
                    self.startpos = (float(x), float(y))
                    found = True
                    break
            if found:
                break
        self.rendpos = (self.endpos[0] * self.scale, self.endpos[1] * self.scale)
        self.rstartpos = (
            -car[0] + self.startpos[0] * self.scale,
            -car[1] + self.startpos[1] * self.scale,
        )
        self.scaled = True

    def draw(self, screen, car, off):
        screen.blit(
            self.scaled_hitbox,
            (-car.x + off[0], -car.y + off[1]),
        )
