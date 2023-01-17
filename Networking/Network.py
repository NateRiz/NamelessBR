from Networking.Client import Client
from Networking.Server import Server


class Network:
    """
    Container for network objects
    """
    def __init__(self):
        self.server: Server | None = None
        self.client: Client | None = None

    def create_host(self):
        """
        Create a server
        """
        self.server = Server()

    def create_client(self, ip, port):
        """
        Create a client and connect to the server
        :param ip: ip of the server
        :param port: port of the server
        """
        self.client = Client()
        self.client.connect(ip, port)
