from Networking.Serializable import Serializable


class ListClientsResponse(Serializable):
    """
    List of ids for all connected clients
    """
    def __init__(self, clients=None):
        self.clients = clients
