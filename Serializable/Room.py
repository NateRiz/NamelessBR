from Networking.Serializable import Serializable


class Room(Serializable):
    def __init__(self, position=(-1, -1)):
        self.position = position
