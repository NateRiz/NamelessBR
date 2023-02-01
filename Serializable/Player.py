from Networking.Serializable import Serializable


class Player(Serializable):
    def __init__(self, position=None, map_coordinates=None):
        self.position = position
        self.map_coordinates = map_coordinates
