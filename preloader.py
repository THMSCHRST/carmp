import threading, queue, pygame
from collections import OrderedDict


class Preloader:
    def __init__(self, index, name, max_cache=10):
        self.index = index
        self.requests = queue.Queue()
        self.cache = OrderedDict()  # maps (x, y) -> surface
        self.max_cache = max_cache
        self.thread = threading.Thread(target=self._worker, daemon=True)
        self.thread.start()
        self.name = name

    def request(self, x, y):
        """Call this from the main thread to queue a tile for loading."""
        if (x, y) not in self.cache:
            self.requests.put((x, y))

    def get(self, x, y):
        """Return the loaded surface or None if not yet loaded."""
        return self.cache.get((x, y), None)

    def _worker(self):
        while True:
            x, y = self.requests.get()
            try:
                surf = pygame.image.load(
                    rf"levels\{self.index}\{self.name}\{x}_{y}.png"
                ).convert()
            except Exception as e:
                print(f"[Preloader] Failed loading tile {x,y}: {e}")
                continue

            # insert into cache, mark as most-recently-used
            self.cache[(x, y)] = surf
            self.cache.move_to_end((x, y), last=True)

            # enforce cache size
            if len(self.cache) > self.max_cache:
                oldest = next(iter(self.cache))
                del self.cache[oldest]
