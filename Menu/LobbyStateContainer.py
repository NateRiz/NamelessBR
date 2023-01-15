from Menu.LobbyState import LobbyState


class LobbyStateContainer:
    def __init__(self):
        self.lobby_state = LobbyState.NONE

    def set(self, state):
        self.lobby_state = state
