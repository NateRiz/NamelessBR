from Networking.Serializable import Serializable


class Player(Serializable):
    def __init__(self, position=None):
        self.position = position
