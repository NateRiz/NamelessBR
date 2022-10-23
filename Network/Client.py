import json
import socket
from typing import Dict

from Network.Server import Server


class Client:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(("127.0.0.1", 7777))

    def send(self, message: Dict):
        raw_message = json.dumps(message)
        message_size = len(raw_message)
        padded_message = str(message_size).ljust(Server.HEADER_SIZE)

        self.socket.send(padded_message.encode())
        self.socket.send(raw_message.encode())
        print(f"Send: {message_size} {raw_message}")
