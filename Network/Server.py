import json
import socket
from threading import Thread
from Network.AtomicDeque import AtomicDeque
from collections import deque

from Network.Message import Message


class Server:
    BUF_SIZE = 32
    HEADER_SIZE = 8  # Header contains length of packet

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("127.0.0.1", 7777))
        self.is_accepting_new_connections = True
        self.clients = []
        self.message_queue = AtomicDeque()

        Thread(target=self.listen).start()

    def listen(self):
        max_connections = 1
        self.socket.settimeout(0.25)
        self.socket.listen(max_connections)
        print("Server started..")

        while self.is_accepting_new_connections and len(self.clients) < max_connections:
            try:
                conn, addr = self.socket.accept()
                self.clients.append(conn)
                Thread(target=self.poll, args=(conn, )).start()
                print(f"New connection: {addr}")
            except TimeoutError:
                pass

    def poll(self, client):
        incoming_stream = deque()
        while True:
            message = self.get_next_message(client, incoming_stream)
            self.message_queue.append(Message(self.clients.index(client), message))
            print(f"Server << {message}")
    def get_next_message(self, client, incoming_stream) -> dict:
        header = self.get_bytes_from_stream(self.HEADER_SIZE, client, incoming_stream)
        message_size = int(header.strip())
        data = self.get_bytes_from_stream(message_size, client, incoming_stream)
        return json.loads(data)

    def get_bytes_from_stream(self, num_bytes, client, incoming_stream: deque) -> str:
        buffer = []
        while num_bytes > 0:
            if len(incoming_stream) == 0:
                self.receive_next_packet(client, incoming_stream)
            else:
                data = incoming_stream.popleft()
                if num_bytes < len(data):
                    extra_data = data[num_bytes:]
                    data = data[:num_bytes]
                    incoming_stream.appendleft(extra_data)
                num_bytes -= len(data)
                if data:
                    buffer.append(data)

        if num_bytes < 0:
            print(f"WARNING: remaining bytes are negative: {num_bytes} -- {buffer}")

        return "".join(b.decode() for b in buffer)

    def receive_next_packet(self, client, incoming_stream):
        try:
            data = client.recv(Server.BUF_SIZE)
        except ConnectionError:
            print(f"Connection removed with {socket.gethostbyname(socket.gethostname())}")
            return

        if data:
            incoming_stream.append(data)
