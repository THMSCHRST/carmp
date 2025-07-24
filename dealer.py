import zmq
import pickle


class Client:
    def __init__(self, username):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.DEALER)

        # Give each client a unique identity
        self.socket.setsockopt(zmq.IDENTITY, username.encode())
        self.socket.connect("tcp://localhost:5555")

        # Send handshake
        self.socket.send_multipart([b"", f"handshake{username}".encode()])
        self.cars = []
        print("Client started.")

    def tick(self, car):
        # Send car data
        self.socket.send_multipart(
            [b"", pickle.dumps((car[0], car[1], car[2], car[3], car[4], car[5]))]
        )

        try:
            _, message = self.socket.recv_multipart(flags=zmq.NOBLOCK)
            self.cars = pickle.loads(message)
            # print("Received cars:", self.cars)
        except zmq.Again:
            pass
