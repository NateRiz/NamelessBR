from Networking.Serializable import Serializable


class ServerMetricsResponse(Serializable):
    def __init__(self, actors=None):
        self.actors = actors
