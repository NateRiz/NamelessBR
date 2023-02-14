from Enemy.Body.BaseEnemy import BaseEnemy
from Engine.Actor import Actor
from Engine.CollisionLayer import CollisionLayer
from Engine.DrawLayer import DrawLayer
from Map.Wall import Wall
import Serializable.Projectile


class Projectile(Actor):
    ID_INCREMENTER = -1

    def __init__(self, position, direction):
        super().__init__()
        self.set_draw_layer(DrawLayer.PROJECTILE)
        self.set_collision_layer(CollisionLayer.PROJECTILE)
        self.add_collision_mask(CollisionLayer.WALL)
        self.add_collision_mask(CollisionLayer.ENEMY)
        Projectile.ID_INCREMENTER += 1
        self.my_id = Projectile.ID_INCREMENTER
        self.position = position
        self.direction = direction
        self.damage = 1
        # Once the object is marked for deletion. This is set to true to tell clients to also destroy it
        self.is_destroyed = False

    def on_collide(self, actor: "Actor"):
        if isinstance(actor, Wall):
            self._on_collide_with_wall(actor)

        elif isinstance(actor, BaseEnemy):
            self._on_collide_with_enemy(actor)

    def _on_collide_with_wall(self, _actor):
        self.destroy()

    def _on_collide_with_enemy(self, actor: BaseEnemy):
        actor.change_health(-self.damage)
        self.destroy()

    def destroy(self):
        self.is_destroyed = True
        self.free()

    def get_serialized(self):
        return Serializable.Projectile.Projectile(self.position, self.direction)
