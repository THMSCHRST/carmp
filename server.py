import zmq
import pickle


class Server:
    def __init__(self, username):
        try:
            self.context = zmq.Context()
            self.socket = self.context.socket(zmq.REP)
            self.socket.bind("tcp://*:5555")
            self.clients = {}
            self.hosted = True
            self.cars = False
            print("Host")
        except Exception as e:
            print(f"Error hosting on port: {e}")
            self.hosted = False
            print("Connecting to server…")
            self.context = zmq.Context()
            self.cars = []
            self.socket = self.context.socket(zmq.REQ)
            self.socket.connect("tcp://localhost:5555")
            self.socket.send_string(f"handshake{username}")

    def tick(self, car):
        if self.hosted:
            try:
                message = self.socket.recv(flags=zmq.NOBLOCK)
                print("Received request:", message)
                if b"handshake" in message:
                    username = message.replace(b"handshake", b"").decode()
                    self.clients[username] = None
                else:
                    if message != False:
                        while True:
                            for car in self.cars:
                                if car.id == pickle.loads(message).id:
                                    break
                            self.cars.append(pickle.loads(message))
                self.socket.send(pickle.dumps(self.cars))
            except zmq.Again:
                pass
        else:
            self.socket.send(pickle.dumps((car[0], car[1], car[2])))
            message = self.socket.recv(flags=zmq.NOBLOCK)
            print("Received request:", message)
            self.cars = pickle.loads(message)


if __name__ == "__main__":
    server = Server()
    while True:
        server.tick()
