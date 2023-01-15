import json
import socket
from collections import deque
from threading import Thread
from typing import Dict

from Networking.AtomicDeque import AtomicDeque
from Networking.Message import Message
from Networking.Server import Server


class Client:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.message_queue = AtomicDeque()

    def connect(self, ip, port):
        self.socket.connect((ip, port))
        print("Client started..")
        Thread(target=self._poll).start()

    def send(self, message: Dict):
        raw_message = json.dumps(message)
        message_size = len(raw_message)
        padded_header = str(message_size).ljust(Server.HEADER_SIZE)

        self.socket.send(padded_header.encode())
        self.socket.send(raw_message.encode())
        # print(f"Send: {message_size} {raw_message}")

    def get_next_message(self) -> Message:
        if len(self.message_queue):
            return self.message_queue.popleft()
        return None

    def _poll(self):
        incoming_stream = deque()
        while True:
            message = self._get_next_message(incoming_stream)
            self.message_queue.append(Message(-1, message))
            # print(f"Server << {message}")

    def _get_next_message(self, incoming_stream) -> dict:
        header = self._get_bytes_from_stream(Server.HEADER_SIZE, incoming_stream)
        message_size = int(header.strip())
        data = self._get_bytes_from_stream(message_size, incoming_stream)
        return json.loads(data)

    def _get_bytes_from_stream(self, num_bytes, incoming_stream: deque) -> str:
        buffer = []
        while num_bytes > 0:
            if len(incoming_stream) == 0:
                self._receive_next_packet(incoming_stream)
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

    def _receive_next_packet(self, incoming_stream):
        try:
            data = self.socket.recv(Server.BUF_SIZE)
        except ConnectionError:
            print(f"Connection removed with {socket.gethostbyname(socket.gethostname())}")
            exit(-1)
        if data:
            incoming_stream.append(data)

