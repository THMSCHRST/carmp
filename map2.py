import pygame


class Map:
    def __init__(self, index, car):
        self.start = (0, 255, 255)
        self.end = (255, 255, 255)
        self.rendpos = (0, 0)
        self.rstartpos = (0, 0)
        with open(rf"levels\{index}\options.txt", "r") as file:
            self.scale = float(file.read())
        self.texture = pygame.image.load(rf"levels\{index}\map.png").convert_alpha()

        image = self.texture
        found = False
        for y in range(image.get_height()):
            for x in range(image.get_width()):
                pixel_color = image.get_at((x, y))[:3]  # Get RGB only (ignore alpha)
                if pixel_color == self.end:
                    self.endpos = (float(x), float(y))
                    found = True
                    break
            if found:
                break

        found = False
        for y in range(image.get_height()):
            for x in range(image.get_width()):
                pixel_color = image.get_at((x, y))[:3]  # Get RGB only (ignore alpha)
                if pixel_color == self.start:
                    self.startpos = (float(x), float(y))
                    found = True
                    break
            if found:
                break

        self.rendpos = (self.endpos[0] * self.scale, self.endpos[1] * self.scale)
        self.rstartpos = (
            -car.x + self.startpos[0] * self.scale,
            -car.y + self.startpos[1] * self.scale,
        )

    def draw(self, screen, car, off):
        transformed_img = pygame.transform.scale_by(self.texture, self.scale)
        screen.blit(transformed_img, (-car.x + off[0], -car.y + off[1]))
