from Networking.Serializable import Serializable


class Movement(Serializable):
    """
    Player movement information
    """
    def __init__(self, my_id=-1, pos=None, direction=None):
        self.my_id = my_id
        self.pos = pos
        self.direction = direction
