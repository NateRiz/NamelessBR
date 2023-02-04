import json
import socket
from collections import deque
from threading import Thread
from time import time, sleep
from typing import Dict

from Networking.AtomicDeque import AtomicDeque
from Networking.Message import Message
from Networking.Serializable import Serializable
from Networking.Server import Server


class Client:
    """
    Client to connect over TCP
    """
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.message_queue = AtomicDeque()
        self.metric_last_record_time = time()
        self.metric_num_bytes = 0
        self.metric_last_kb = 0
        self._is_connected = False

    def connect(self, ip, port):
        """
        Tries to connect the client to the server
        :param ip: Ip of host
        :param port: Port of host
        """
        while not self._is_connected:
            try:
                self.socket.connect((ip, port))
                self._is_connected = True
            except socket.error as error:
                print(F"Client connection failed: {error}\nRetrying...")
                sleep(1)
        print("Client started..")
        Thread(target=self._poll).start()

    def send(self, message: Dict[int, Serializable]):
        """
        Sends a json serializable object to the server
        :param message: JSON serializable object
        """
        raw_message = json.dumps(message, default=Serializable.serialize)
        message_size = len(raw_message)
        padded_header = str(message_size).ljust(Server.HEADER_SIZE)
        if '{"3":' not in raw_message:
            print(f"C > {raw_message}")
        self.socket.send(padded_header.encode())
        self.socket.send(raw_message.encode())

    def get_next_message(self) -> Message | None:
        """
        Gets the next message in the queue if there is one.
        :return: next message in the queue
        """
        if len(self.message_queue):
            return self.message_queue.popleft()
        return None

    def is_connected(self):
        return self._is_connected

    def get_incoming_kb_metric(self):
        """
        Accumulates metric for data retrieved per second.
        This must be called every frame by consumer
        :return: Amount of data retrieved in Kb
        """
        if time() - self.metric_last_record_time > 1:
            self.metric_last_record_time = time()
            self.metric_last_kb = self.metric_num_bytes
            self.metric_num_bytes = 0
        return round(self.metric_last_kb / 1024, 2)

    def _poll(self):
        incoming_stream = deque()
        while True:
            message = self._get_next_message(incoming_stream)
            self.message_queue.append(Message(-1, message))

    def _get_next_message(self, incoming_stream) -> dict:
        header = self._get_bytes_from_stream(Server.HEADER_SIZE, incoming_stream)
        message_size = int(header.strip())
        data = self._get_bytes_from_stream(message_size, incoming_stream)
        self.metric_num_bytes += len(data)
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
            if data:
                incoming_stream.append(data)
        except ConnectionError:
            print(f"Connection removed with {socket.gethostbyname(socket.gethostname())}")
            exit(-1)
