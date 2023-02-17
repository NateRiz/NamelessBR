class Movement:
    """
    Player movement information
    """
    def __init__(self, my_id=-1, pos=None, direction=None, angle=None):
        self.my_id = my_id
        self.pos = pos
        self.direction = direction
        self.angle = angle
