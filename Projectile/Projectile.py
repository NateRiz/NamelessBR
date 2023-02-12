from Enemy.Body.BaseEnemy import BaseEnemy
from Engine.Actor import Actor
from Engine.CollisionLayer import CollisionLayer
from Engine.DrawLayer import DrawLayer
from Map.Wall import Wall
import Serializable.Projectile


class Projectile(Actor):
    def __init__(self, position, direction):
        super().__init__()
        self.set_draw_layer(DrawLayer.PROJECTILE)
        self.set_collision_layer(CollisionLayer.PROJECTILE)
        self.add_collision_mask(CollisionLayer.WALL)
        self.add_collision_mask(CollisionLayer.ENEMY)
        self.position = position
        self.direction = direction

    def on_collide(self, actor: "Actor"):
        if isinstance(actor, Wall):
            self._on_collide_with_wall(actor)
        elif isinstance(actor, BaseEnemy):
            self._on_collide_with_wall(actor)

    def _on_collide_with_wall(self, _actor):
        self.free()

    def get_serialized(self):
        return Serializable.Projectile.Projectile(self.position, self.direction)
