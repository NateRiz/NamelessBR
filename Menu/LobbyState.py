from enum import Enum


class LobbyState(Enum):
    MENU = 0
    PLAY = 1
    HOST = 2
    JOIN = 3