import pygame
from math import *
import random

pygame.init()
pygame.joystick.init()

joystick = None
# Initialize the first controller
if pygame.joystick.get_count() == 0:
    print("No controller connected!")
else:
    joystick = pygame.joystick.Joystick(0)
    print(f"Detected controller: {joystick.get_name()}")


def move_in_direction(x, y, angle_degrees, distance):
    angle_radians = radians(angle_degrees)
    new_x = x + cos(angle_radians) * distance
    new_y = y - sin(angle_radians) * distance
    return new_x, new_y


class Car:
    def __init__(self, x, y, r, xo, yo):
        self.id = random.randint(1, 1000)
        self.x, self.y = x, y
        self.r = r
        self.v = 0
        self.xv = 0
        self.yv = 0
        self.rv = 0
        self.xo = xo
        self.yo = yo
        self.handling = 19
        self.power = 2
        self.drift = 8
        self.l1 = pygame.image.load(r"assets\pl1.png").convert_alpha()
        self.l2 = pygame.image.load(r"assets\pl2.png").convert_alpha()
        self.l3 = pygame.image.load(r"assets\pl3.png").convert_alpha()
        self.l4 = pygame.image.load(r"assets\pl4.png").convert_alpha()
        self.l5 = pygame.image.load(r"assets\pl5.png").convert_alpha()

    def draw(self, screen):
        self.r -= 90
        for i in range(5):
            rotated = pygame.transform.rotate(self.l1, self.r)

            transformed_img = pygame.transform.scale_by(rotated, 2.5)

            rect = transformed_img.get_rect(center=(self.xo, self.yo - i))

            screen.blit(transformed_img, rect)

        for i in range(3):
            rotated = pygame.transform.rotate(self.l2, self.r)

            transformed_img = pygame.transform.scale_by(rotated, 2.5)

            rect = transformed_img.get_rect(center=(self.xo, self.yo - i - 5))

            screen.blit(transformed_img, rect)

        for i in range(2):
            rotated = pygame.transform.rotate(self.l3, self.r)

            transformed_img = pygame.transform.scale_by(rotated, 2.5)

            rect = transformed_img.get_rect(center=(self.xo, self.yo - i - 10))

            screen.blit(transformed_img, rect)

        for i in range(5):
            rotated = pygame.transform.rotate(self.l4, self.r)

            transformed_img = pygame.transform.scale_by(rotated, 2.5)

            rect = transformed_img.get_rect(center=(self.xo, self.yo - i - 15))

            screen.blit(transformed_img, rect)

        for i in range(1):
            rotated = pygame.transform.rotate(self.l5, self.r)

            transformed_img = pygame.transform.scale_by(rotated, 2.5)

            rect = transformed_img.get_rect(center=(self.xo, self.yo - i - 20))

            screen.blit(transformed_img, rect)
        self.r += 90

    def tick(self):  # 1 to 1 copy from old car code
        keys = pygame.key.get_pressed()
        if not joystick:
            if keys[pygame.K_w]:
                self.v += 0.5  # step 1
            if keys[pygame.K_a]:
                self.rv += (self.v / (21 - self.handling)) / 2
            if keys[pygame.K_d]:
                self.rv -= (self.v / (21 - self.handling)) / 2
            if keys[pygame.K_s]:
                self.v -= 0.5
        else:
            left_x = round(joystick.get_axis(0), 3)
            self.rv -= ((self.v / (21 - self.handling)) / 2) * left_x * 2
            rt = round(joystick.get_axis(5), 3)
            lt = round(joystick.get_axis(4), 3)
            self.v += 0.5 * max(rt, 0)
            self.v -= 0.5 * max(lt, 0)
        self.r += self.rv
        self.rv *= 0.95
        xdiff, ydiff = move_in_direction(self.x, self.y, self.r, self.v)  # step 4
        self.xv += xdiff - self.x
        self.yv += ydiff - self.y
        self.x += self.xv
        self.y += self.yv
        self.xv -= (self.xv / self.drift) / 2
        self.yv -= (self.yv / self.drift) / 2
        self.v -= self.v / self.power


def draw(screen, xo, yo, r, l1, l2, l3, l4, l5, scale=2.5):
    # print("from carr", xo, yo, xo, yo)
    r -= 90
    frect = None
    for i in range(5):
        rotated = pygame.transform.rotate(l1, r)

        transformed_img = pygame.transform.scale_by(rotated, scale)

        rect = transformed_img.get_rect(center=(xo, yo - i))
        frect = rect
        screen.blit(transformed_img, rect)

    for i in range(3):
        rotated = pygame.transform.rotate(l2, r)

        transformed_img = pygame.transform.scale_by(rotated, scale)

        rect = transformed_img.get_rect(center=(xo, yo - i - 5))

        screen.blit(transformed_img, rect)

    for i in range(2):
        rotated = pygame.transform.rotate(l3, r)

        transformed_img = pygame.transform.scale_by(rotated, scale)

        rect = transformed_img.get_rect(center=(xo, yo - i - 10))

        screen.blit(transformed_img, rect)

    for i in range(5):
        rotated = pygame.transform.rotate(l4, r)

        transformed_img = pygame.transform.scale_by(rotated, scale)

        rect = transformed_img.get_rect(center=(xo, yo - i - 15))

        screen.blit(transformed_img, rect)

    for i in range(1):
        rotated = pygame.transform.rotate(l5, r)

        transformed_img = pygame.transform.scale_by(rotated, scale)

        rect = transformed_img.get_rect(center=(xo, yo - i - 20))

        screen.blit(transformed_img, rect)
    r += 90
    return frect
