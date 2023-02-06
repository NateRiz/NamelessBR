from enum import IntEnum


class CollisionLayer(IntEnum):
    """This is the layer that an object appears in. ie: Player object is in player layer."""
    NONE = 0
    PLAYER = 1
    PROJECTILE = 2
    WALL = 3
    ENEMY = 4
