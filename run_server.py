from router import Server
import time

server = Server()

while True:
    server.tick()
    time.sleep(0.01)
