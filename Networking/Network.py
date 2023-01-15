from Networking.Client import Client
from Networking.Server import Server


class Network:
    def __init__(self):
        self.server: Server = None
        self.client: Client = None

    def create_host(self):
        self.server = Server()

    def create_client(self, ip, port):
        self.client = Client(ip, port)
