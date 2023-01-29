from enum import IntEnum


class DrawLayer(IntEnum):
    """
    Layers for sorted z-index drawing. Drawn in increasing order
    """
    NONE = 0
    GROUND = 1
    STRUCTURE = 2
    ENEMY = 3
    ENEMY_PLAYER = 4
    PROJECTILE = 5
    # Objects draw themselves to a room and the room draws the objects at the end of the frame.
    ROOM = 6
    PLAYER = 7
    DEBUG = 8
