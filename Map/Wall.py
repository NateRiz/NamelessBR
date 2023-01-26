from Engine.Actor import Actor


class Wall(Actor):
    def __init__(self, rect):
        super().__init__()
        self.rect = rect
