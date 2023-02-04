from Engine.Actor import Actor
from Engine.CollisionLayer import CollisionLayer


class Wall(Actor):
    def __init__(self, rect):
        super().__init__()
        self.set_collision_layer(CollisionLayer.WALL)
        self.rect = rect
