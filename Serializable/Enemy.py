from Networking.Serializable import Serializable


class Enemy(Serializable):
    def __init__(self, enemy_type=None, position=None):
        self.enemy_type = enemy_type
        self.position = position
