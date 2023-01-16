from Networking.Serializable import Serializable


class Movement(Serializable):
    def __init__(self, my_id=-1, pos=None, direction=None):
        if pos is None:
            pos = []
        if direction is None:
            direction = []
        self.my_id = my_id
        self.pos = pos
        self.direction = direction
