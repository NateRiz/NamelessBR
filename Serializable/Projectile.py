from Networking.Serializable import Serializable


class Projectile(Serializable):
    def __init__(self, position=None, direction=None):
        self.position = position
        self.direction = direction
