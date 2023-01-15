import json
import socket
from typing import Dict

from Networking.Server import Server


class Client:
    def __init__(self, ip, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ip, port))

    def send(self, message: Dict):
        raw_message = json.dumps(message)
        message_size = len(raw_message)
        padded_message = str(message_size).ljust(Server.HEADER_SIZE)

        self.socket.send(padded_message.encode())
        self.socket.send(raw_message.encode())
        print(f"Send: {message_size} {raw_message}")
