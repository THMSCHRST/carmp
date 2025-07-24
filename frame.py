# fix resize causing client server pos desync

import pygame
from colors import C
from car import Car, move_in_direction, draw
from map2 import Map
import math
import random
from particle import Particle
from dealer import Client

# particles lift storing all the particles
particles = []

# initialize pygame
pygame.init()

# define window settings
WIDTH, HEIGHT = 800, 800
FPS = 60

# create window and clock
screen = pygame.display.set_mode((WIDTH, HEIGHT), vsync=True, flags=pygame.RESIZABLE)
pygame.display.set_caption("CAR")
clock = pygame.time.Clock()

# load car assets for car.draw()
l1 = pygame.image.load(r"assets\pl1.png").convert_alpha()
l2 = pygame.image.load(r"assets\pl2.png").convert_alpha()
l3 = pygame.image.load(r"assets\pl3.png").convert_alpha()
l4 = pygame.image.load(r"assets\pl4.png").convert_alpha()
l5 = pygame.image.load(r"assets\pl5.png").convert_alpha()

# player pos (unused)
x, y = 0, 0

# define car and map renderer
car = Car(0, 0, 90, WIDTH / 2, HEIGHT / 2)
level = Map(3, car)


# define interpolation function
def lerp(a, b, t):
    return (1 - t) * a + t * b


# define function to get distance between two vectors
def distance(a, b):
    return math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)


# draw a line between two vectors
def line(color, p1, p2, thickness):
    tp1 = (p1[0] + x, p1[1] + y)
    tp2 = (p2[0] + x, p2[1] + y)
    pygame.draw.line(screen, color, tp1, tp2, thickness)


# argument used for one time spawning
spawned = False

# old velocity and old position
oldvel = (0, 0)
oldpos = (0, 0)

# define client (does the networking)
client = Client(f"user{random.randint(1,999)}")

# last velocity and position of all cars
carvelmp = {}
oldcarvelmp = {}  # 1 frame older than carvelmp
carposmp = {}

# bool used for 30fps networking
send = True

running = True
while running:
    # make car centered client side and server side when the window is resized
    if car.xo != screen.get_width() / 2 or car.yo != screen.get_height() / 2:
        car.x += (screen.get_width() / 2) - car.xo
        car.y += (screen.get_width() / 2) - car.yo
        car.xo = screen.get_width() / 2
        car.yo = screen.get_height() / 2
    # update x,y clientside
    x, y = car.x, car.y

    # update listener
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # backgorund
    screen.fill(C.gray)

    # spawn the player at correct pos
    if not spawned:
        car.x, car.y = level.rstartpos[0] - car.xo, level.rstartpos[1] - car.yo
        oldpos = (car.x, car.y)
        spawned = True

    # render the map
    level.draw(screen, car)

    # render particles
    for p in particles[:]:
        p.tick(screen, car)
        if not p.life:
            particles.remove(p)

    # update car
    car.tick()
    # render car
    car.draw(screen)

    # do client networking every secon frame
    if send:
        for item in client.cars:
            if item[3] != car.id:
                carposmp[item[3]] = (item[0], item[1])
        client.tick((round(car.x), round(car.y), round(car.r), car.id, car.xv, car.yv))
        send = False
    else:
        send = True  # update send

    for item in client.cars:
        if item[3] != car.id:  # if car not self
            try:
                # set postition for particle spawn dependant on update tick/no update tick
                if send or carposmp == {}:
                    particlepos = (item[0], item[1])
                else:
                    # interpolat particle pos
                    particlepos = (
                        lerp(
                            carposmp[item[3]][0],
                            item[0],
                            0.5,
                        ),
                        lerp(carposmp[item[3]][1], item[1], 0.5),
                    )
                if send or carvelmp == {}:
                    if (
                        # spawn cloud particle at high interpolated acceleration
                        min(
                            distance(
                                (
                                    lerp(
                                        oldcarvelmp[item[3]][0],
                                        carvelmp[item[3]][0],
                                        0.5,
                                    ),
                                    lerp(
                                        oldcarvelmp[item[3]][1],
                                        carvelmp[item[3]][1],
                                        0.5,
                                    ),
                                ),
                                (
                                    lerp(carvelmp[item[3]][0], item[4], 0.5),
                                    lerp(carvelmp[item[3]][1], item[5], 0.5),
                                ),
                            ),
                            150,
                        )
                        > random.randint(15, 150) / 100
                    ):
                        particles.append(
                            Particle(
                                "cloud",
                                particlepos[0] + car.xo,
                                particlepos[1] + car.yo,
                                2.5,
                                (-5, -13),
                                0.5,
                            )
                        )
                    if (
                        # spawn cloud2 particle at high interpolated acceleration
                        min(
                            distance(
                                (
                                    lerp(
                                        oldcarvelmp[item[3]][0],
                                        carvelmp[item[3]][0],
                                        0.5,
                                    ),
                                    lerp(
                                        oldcarvelmp[item[3]][1],
                                        carvelmp[item[3]][1],
                                        0.5,
                                    ),
                                ),
                                (
                                    lerp(carvelmp[item[3]][0], item[4], 0.5),
                                    lerp(carvelmp[item[3]][1], item[5], 0.5),
                                ),
                            ),
                            150,
                        )
                        > random.randint(25, 150) / 100
                    ):
                        particles.append(
                            Particle(
                                "cloud2",
                                particlepos[0] + car.xo,
                                particlepos[1] + car.yo,
                                2.5,
                                (-5, -13),
                                0.5,
                            )
                        )
                    if (
                        # spawn tire particle at high interpolated acceleration
                        min(
                            distance(
                                (
                                    lerp(
                                        oldcarvelmp[item[3]][0],
                                        carvelmp[item[3]][0],
                                        0.5,
                                    ),
                                    lerp(
                                        oldcarvelmp[item[3]][1],
                                        carvelmp[item[3]][1],
                                        0.5,
                                    ),
                                ),
                                (
                                    lerp(carvelmp[item[3]][0], item[4], 0.5),
                                    lerp(carvelmp[item[3]][1], item[5], 0.5),
                                ),
                            ),
                            150,
                        )
                        > 0.75
                    ):
                        particles.append(
                            Particle(
                                "tire",
                                particlepos[0] + car.xo,
                                particlepos[1] + car.yo,
                                2.5,
                                (-5, -13),
                                0,
                                (120, 240),
                            )
                        )
                else:
                    if (
                        min(distance(carvelmp[item[3]], (item[4], item[5])), 150)
                        > random.randint(15, 150) / 100
                    ):
                        particles.append(
                            Particle(
                                "cloud",
                                particlepos[0] + car.xo,
                                particlepos[1] + car.yo,
                                2.5,
                                (-5, -13),
                                0.5,
                            )
                        )
                    if (
                        min(distance(carvelmp[item[3]], (item[4], item[5])), 150)
                        > random.randint(25, 150) / 100
                    ):
                        particles.append(
                            Particle(
                                "cloud2",
                                particlepos[0] + car.xo,
                                particlepos[1] + car.yo,
                                2.5,
                                (-5, -13),
                                0.5,
                            )
                        )
                    if min(distance(carvelmp[item[3]], (item[4], item[5])), 150) > 1.5:
                        particles.append(
                            Particle(
                                "tire",
                                particlepos[0] + car.xo,
                                particlepos[1] + car.yo,
                                2.5,
                                (-5, -13),
                                0,
                                (120, 240),
                            )
                        )
            except Exception as e:
                print(e)
            if item[3] in carvelmp:
                oldcarvelmp[item[3]] = carvelmp[item[3]]
            carvelmp[item[3]] = (item[4], item[5])

            # draw car after network update
            if send or carposmp == {}:
                draw(
                    screen,
                    -car.x + item[0] + car.xo,
                    -car.y + item[1] + car.yo,
                    item[2],
                    l1,
                    l2,
                    l3,
                    l4,
                    l5,
                )
            # draw car interpolated (cuz no network update)
            else:
                draw(
                    screen,
                    -car.x + lerp(carposmp[item[3]][0], item[0], 0.5) + car.xo,
                    -car.y + lerp(carposmp[item[3]][1], item[1], 0.5) + car.yo,
                    item[2],
                    l1,
                    l2,
                    l3,
                    l4,
                    l5,
                )

    # spawn cloud1 particle at high acceleration
    if min(distance(oldvel, (car.xv, car.yv)), 150) > random.randint(15, 150) / 100:
        particles.append(
            Particle(
                "cloud",
                move_in_direction(
                    oldpos[0] + car.xo, oldpos[1] + car.yo, car.r - 90, 0
                )[0],
                move_in_direction(
                    oldpos[0] + car.xo, oldpos[1] + car.yo, car.r - 90, 0
                )[1],
                2.5,
                (-5, -13),
                0.5,
            )
        )

    # spawn cloud2 particle at high acceleration
    if min(distance(oldvel, (car.xv, car.yv)), 150) > random.randint(25, 150) / 100:
        particles.append(
            Particle(
                "cloud2",
                move_in_direction(
                    oldpos[0] + car.xo, oldpos[1] + car.yo, car.r - 90, 0
                )[0],
                move_in_direction(
                    oldpos[0] + car.xo, oldpos[1] + car.yo, car.r - 90, 0
                )[1],
                2.5,
                (-5, -13),
                0.5,
            )
        )

    # spawn tire particle at high acceleration
    if min(distance(oldvel, (car.xv, car.yv)), 150) > 0.75:
        particles.append(
            Particle(
                "tire",
                move_in_direction(
                    oldpos[0] + car.xo, oldpos[1] + car.yo, car.r - 90, 0
                )[0],
                move_in_direction(
                    oldpos[0] + car.xo, oldpos[1] + car.yo, car.r - 90, 0
                )[1],
                2.5,
                (-5, -13),
                0,
                (120, 240),
            )
        )

    oldvel = (car.xv, car.yv)  # update old vel and pos
    oldpos = (car.x, car.y)

    # next gametick
    pygame.display.update()
    clock.tick(FPS)

# fully exit program if running in idle
pygame.quit()
