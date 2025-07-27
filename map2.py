import pygame
import time
import os
from functools import lru_cache
from preloader import Preloader
import threading
import time
from tilechache import TileCache


class Map:
    def __init__(self, index, car):
        self.start = (0, 255, 255)
        self.end = (255, 255, 255)
        self.rendpos = (0, 0)
        self.rstartpos = (0, 0)
        self.scaled = False
        self.tiles2 = []
        self.scaled2 = False
        self.startpos = ()
        self.tilechache2 = {}
        self.endpos = []
        self.savetemp = []
        with open(rf"levels\{index}\options.txt", "r") as file:
            self.scale = float(file.read())
        self.index = index
        # self.overlay = pygame.image.load(rf"levels\{index}\map.png").convert_alpha()

    @lru_cache(maxsize=8)  # keep 100 tiles in memory
    def load_tile(self, x, y):
        return pygame.image.load(rf"levels\{self.index}\tilesmap\{x}_{y}.png").convert()

    def image_to_tiles(self, image: pygame.Surface, tile_size: int):
        print(f"[DEBUG] Image size: {image.get_size()}, Tile size: {tile_size}")
        tiles = []
        img_w, img_h = image.get_size()

        for y in range(0, img_h, tile_size):
            for x in range(0, img_w, tile_size):
                width = min(tile_size)
                height = min(tile_size)

                rect = pygame.Rect(x, y, width, height)

                if rect.right <= img_w and rect.bottom <= img_h:
                    sub = image.subsurface(rect).copy()
                    tiles.append((sub, x, y))
                    print(f"[TILE] Added tile at ({x}, {y})")
                else:
                    print(f"[TILE] Skipped out-of-bounds tile at ({x}, {y})")

        return tiles

    def slice_step(self):
        if hasattr(self, "slicing_queue") and self.slicing_queue:
            x, y = self.slicing_queue.pop(0)
            img_w = self.hitbox.get_width()
            img_h = self.hitbox.get_height()

            if x >= img_w or y >= img_h:
                return

            w = min(512, img_w - x)
            h = min(512, img_h - y)

            if w <= 0 or h <= 0:
                return

            try:
                tile = self.hitbox.subsurface(pygame.Rect(x, y, w, h))
                scaled_tile = pygame.transform.scale_by(tile, self.scale)
                self.tiles.append((scaled_tile, x * self.scale, y * self.scale))
                print(
                    f"[TILE] Added scaled tile at ({x * self.scale}, {y * self.scale})"
                )
            except Exception as e:
                print(f"[TILE] Error at ({x},{y}): {e}")

        elif not self.slicing_queue:
            self.scaled = True
            print("Finished slicing")

    def slice_step2(self):
        if hasattr(self, "slicing_queue2") and self.slicing_queue2:
            saved = os.path.exists(rf"levels\{self.index}\tilesmap")
            x, y = self.slicing_queue2.pop(0)
            img_w = self.map.get_width()
            img_h = self.map.get_height()

            if x >= img_w or y >= img_h:
                return

            w = min(512, img_w - x)
            h = min(512, img_h - y)

            if w <= 0 or h <= 0:
                return

            try:
                tile = self.map.subsurface(pygame.Rect(x, y, w, h))
                scaled_tile = pygame.transform.scale_by(tile, self.scale)
                if not saved:
                    self.savetemp.append((scaled_tile, x * self.scale, y * self.scale))
                self.tiles2.append((None, x * self.scale, y * self.scale))
                print(
                    f"[TILE] Added scaled tile at ({x * self.scale}, {y * self.scale})"
                )
            except Exception as e:
                print(f"[TILE] Error at ({x},{y}): {e}")

        if not self.slicing_queue2 and self.savetemp:
            if not saved:
                os.makedirs(f"levels/{self.index}/tilesmap", exist_ok=True)
                for tile, sx, sy in self.savetemp:
                    print("saving")
                    pygame.image.save(
                        tile, f"levels/{self.index}/tilesmap/{sx}_{sy}.png"
                    )
            self.savetemp.clear()
            self.scaled2 = True
            print("Finished slicing and saved all tiles")

    def scalef(self, car):
        rlstart = time.time()
        print("Asset init started...")
        print("importing hitbox...")
        start = time.time()
        self.hitbox = pygame.image.load(
            rf"levels\{self.index}\hitbox.png"
        ).convert_alpha()
        self.map = pygame.image.load(rf"levels\{self.index}\map.png").convert_alpha()
        print(f"finished {time.time()-start}")
        print("scaling hitbox...")
        start = time.time()
        # self.scaled_hitbox = pygame.transform.scale_by(
        #    self.hitbox, self.scale
        # ).convert_alpha()
        print(f"finished {time.time()-start}")
        print("creating scaled rect...")
        start = time.time()
        # self.scaled_rect = self.scaled_hitbox.get_rect()
        print(f"finished {time.time()-start}")
        image = self.hitbox
        print("finding goal...")
        start = time.time()
        found = False
        if os.path.exists(rf"levels\{self.index}\chache.txt"):
            print("cache exists...")
            with open(rf"levels\{self.index}\chache.txt", "r") as file:
                numbers = tuple(int(round(float(line.strip()), 0)) for line in file)
                self.startpos = (numbers[0], numbers[1])
                self.endpos = (numbers[2], numbers[3])

        else:
            for y in range(image.get_height()):
                for x in range(image.get_width()):
                    pixel_color = image.get_at((x, y))[:3]
                    if pixel_color == self.start:
                        self.startpos = (float(x), float(y))
                        found = True
                        break
                if found:
                    break
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
            with open(rf"levels\{self.index}\chache.txt", "w") as file:
                file.write(
                    str(self.startpos[0])
                    + "\n"
                    + str(self.startpos[1])
                    + "\n"
                    + str(self.endpos[0])
                    + "\n"
                    + str(self.endpos[1])
                )
        print(f"finished {time.time()-start}")
        print("finding spawn...")
        print(f"finished {time.time()-start}")
        print("calculating goal and spawn...")
        start = time.time()
        self.rendpos = (self.endpos[0] * self.scale, self.endpos[1] * self.scale)
        self.rstartpos = (
            -car[0] + self.startpos[0] * self.scale,
            -car[1] + self.startpos[1] * self.scale,
        )
        print(f"finished {time.time()-start}")
        print("hitbox:")
        print(self.hitbox)
        print("scaled hitbox:")
        # print(self.scaled_hitbox)
        print("calculating tiles...")
        start = time.time()
        # self.tiles = self.image_to_tiles(self.scaled_hitbox, 512)  # unused
        # make tile slicing queue
        self.slicing_queue = []
        tile_size = 512
        for y in range(0, self.hitbox.get_height(), tile_size):
            for x in range(0, self.hitbox.get_width(), tile_size):
                self.slicing_queue.append((x, y))

        self.tiles = []
        print(f"finished {time.time()-start}")
        # self.scaled = True
        self.slicing_queue2 = []
        tile_size = 512
        self.tile_size = tile_size
        for y in range(0, self.map.get_height(), tile_size):
            for x in range(0, self.map.get_width(), tile_size):
                self.slicing_queue2.append((x, y))
        self.preloader2 = Preloader(self.index)
        self.preloader2t = threading.Thread(target=self.preloader2._worker, daemon=True)
        self.preloader2t.start()

        self.tiles2 = []
        print(f"finished {time.time()-start}")
        # self.scaled = True
        print(f"finished init in {time.time()-rlstart}")

    def draw(self, screen, car, off):
        screen.blit(
            self.scaled_hitbox,
            (-car.x + off[0], -car.y + off[1]),
        )

    def draw_tiles(self, screen, car, off):
        for tile, x, y in self.tiles:
            if (
                x > (car.x - ((self.tile_size * self.scale * 2) + 1))
                and x < (car.x + screen.get_width())
                and y < (car.y + screen.get_height())
                and y > (car.y - ((self.tile_size * self.scale * 2) + 1))
            ):
                screen.blit(tile, (-car.x + off[0] + x, -car.y + off[1] + y))

    def draw_tiles2(self, screen, car, off):
        screen_w, screen_h = screen.get_size()
        ts = self.tile_size * self.scale

        for _, x, y in self.tiles2:
            # visibility check
            if (
                x > car.x - (ts * 2)
                and x < car.x + screen_w
                and y > car.y - (ts * 2)
                and y < car.y + screen_h
            ):
                # queue it for loading if not in cache
                if not self.preloader2.get(x, y):
                    self.preloader2.request(x, y)
                else:
                    # blit immediately if loaded
                    surf = self.preloader2.get(x, y)
                    self.tilechache2[f"{str(x) + str(y)}"] = surf
                if f"{str(x) + str(y)}" in self.tilechache2:
                    screen.blit(
                        self.tilechache2[f"{str(x) + str(y)}"],
                        (-car.x + off[0] + x, -car.y + off[1] + y),
                    )
