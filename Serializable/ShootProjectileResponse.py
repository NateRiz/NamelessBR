from Networking.Serializable import Serializable


class ShootProjectileResponse(Serializable):
    def __init__(self, my_id=None, position=None, direction=None):
        self.my_id = my_id
        self.position = position
        self.direction = direction
