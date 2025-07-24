import zmq
import pickle
import time


class Server:
    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.ROUTER)
        self.socket.bind("tcp://*:5555")
        self.clients = {}
        self.cars = []
        self.timeout = {}
        print("Server started.")

    def tick(self):
        try:
            # ROUTER sockets prepend a client identity
            identity, empty, message = self.socket.recv_multipart(flags=zmq.NOBLOCK)
            print(f"Received from {identity}: {message}")

            if b"handshake" in message:
                username = message.replace(b"handshake", b"").decode()
                self.clients[username] = identity
                print(f"Handshake from {username}")
            else:
                car = pickle.loads(message)
                # Replace car with same ID or add new
                found = False
                self.timeout[car[3]] = time.time()
                for i, c in enumerate(self.cars):
                    if c[3] == car[3]:
                        self.cars[i] = car
                        found = True
                        break
                if not found:
                    self.cars.append(car)
            for item in self.timeout:
                if self.timeout[item] + 5 < time.time():
                    for car in self.cars:
                        if car[3] == item:
                            print(f"Timeout {car}")
                            self.cars.remove(car)
                            break

            # Respond to client
            self.socket.send_multipart([identity, b"", pickle.dumps(self.cars)])

        except zmq.Again:
            pass
