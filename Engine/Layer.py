from enum import IntEnum


class Layer(IntEnum):
    """
    Layers for sorted z-index drawing. Drawn in increasing order
    """
    NONE = 0
    GROUND = 1
    STRUCTURE = 2
    ENEMY = 3
    ENEMY_PLAYER = 4
    # Objects draw themselves to a room and the room draws the objects at the end of the frame.
    ROOM = 5
    PLAYER = 6
    DEBUG = 7
