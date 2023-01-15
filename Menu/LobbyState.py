from enum import Enum


class LobbyState(Enum):
    NONE = 0
    TRANSITION_TO_MENU = 1
    MENU = 2
    TRANSITION_TO_GAME = 3
    GAME = 4
    TRANSITION_TO_HOST = 5
    HOST = 6
    TRANSITION_TO_JOIN = 7
    JOIN = 8
