import json
import socket
from threading import Thread
from typing import Dict

from Networking.AtomicDeque import AtomicDeque
from collections import deque
from time import time

from Networking.Message import Message
from Networking.Serializable import Serializable


class Server:
    BUF_SIZE = 32
    HEADER_SIZE = 8  # Header contains length of packet

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("127.0.0.1", 7777))
        self.is_accepting_new_connections = True
        self.clients = {}
        self.message_queue = AtomicDeque()
        self.metric_last_record_time = time()
        self.metric_num_bytes = 0
        self.metric_last_kb = 0

        Thread(target=self._listen).start()

    def get_next_message(self) -> Message:
        if len(self.message_queue):
            return self.message_queue.popleft()
        return None

    def get_incoming_kb_metric(self):
        if time() - self.metric_last_record_time > 1:
            self.metric_last_record_time = time()
            self.metric_last_kb = self.metric_num_bytes
            self.metric_num_bytes = 0
        return round(self.metric_last_kb / 1024, 2)

    def send(self, message: Dict, owner_id):
        padded_header, raw_message = self._encode_message(message)
        print(F"S>{owner_id}: {message}")

        self.clients[owner_id].send(padded_header)
        self.clients[owner_id].send(raw_message)

    def send_all(self, message: Dict):
        padded_header, raw_message = self._encode_message(message)
        print(F"SV>A: {message}")

        for owner_id, conn in self.clients.items():
            conn.send(padded_header)
            conn.send(raw_message)

    def send_all_except(self, message: Dict, excluded_id):
        padded_header, raw_message = self._encode_message(message)
        print(F"SV>A-{excluded_id}: {message}")
        for owner_id, conn in self.clients.items():
            if owner_id != excluded_id:
                conn.send(padded_header)
                conn.send(raw_message)

    def _encode_message(self, message):
        raw_message = json.dumps(message, default=Serializable.serialize)
        message_size = len(raw_message)
        padded_header = str(message_size).ljust(Server.HEADER_SIZE)
        return padded_header.encode(), raw_message.encode()

    def _listen(self):
        max_connections = 5
        client_id_incrementer = 0
        # self.socket.settimeout(0.25)
        self.socket.listen(max_connections)
        print("Server started..")

        while self.is_accepting_new_connections and len(self.clients) < max_connections:
            try:
                conn, addr = self.socket.accept()
                print(conn)
                self.clients[client_id_incrementer] = conn
                Thread(target=self._poll, args=(conn, client_id_incrementer)).start()
                client_id_incrementer += 1
                print(f"New connection: {addr}")
            except TimeoutError:
                pass

    def _poll(self, client, owner_id):
        incoming_stream = deque()
        while True:
            message = self._get_next_message(client, incoming_stream)
            self.message_queue.append(Message(owner_id, message))

    def _get_next_message(self, client, incoming_stream) -> dict:
        header = self._get_bytes_from_stream(Server.HEADER_SIZE, client, incoming_stream)
        message_size = int(header.strip())
        data = self._get_bytes_from_stream(message_size, client, incoming_stream)
        self.metric_num_bytes += len(data)
        return json.loads(data)

    def _get_bytes_from_stream(self, num_bytes, client, incoming_stream: deque) -> str:
        buffer = []
        while num_bytes > 0:
            if len(incoming_stream) == 0:
                self._receive_next_packet(client, incoming_stream)
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

    def _receive_next_packet(self, client, incoming_stream):
        try:
            data = client.recv(Server.BUF_SIZE)
            if data:
                incoming_stream.append(data)
        except ConnectionError:
            print(f"Connection removed with {socket.gethostbyname(socket.gethostname())}")
            return
        except TimeoutError:
            print("Server socket timeout")
            pass
