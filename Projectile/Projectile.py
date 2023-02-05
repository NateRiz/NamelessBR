from Engine.Actor import Actor
from Engine.CollisionLayer import CollisionLayer
from Engine.DrawLayer import DrawLayer


class Projectile(Actor):
    def __init__(self, position, direction):
        super().__init__()
        self.set_draw_layer(DrawLayer.PROJECTILE)
        self.set_collision_layer(CollisionLayer.PROJECTILE)
        self.add_collision_mask(CollisionLayer.WALL)
        self.position = position
        self.direction = direction

    def on_collide(self, actor: "Actor"):
        self.free()
