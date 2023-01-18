from Menu.LobbyState import LobbyState


class LobbyStateContainer:
    """
    Container for passing the same instance to multiple objects.
    Each lobby will change this to the next state.
    """
    def __init__(self):
        self.lobby_state = LobbyState.NONE

    def set(self, state):
        """
        Sets the state to the specified lobby state
        :param state: state to set to
        """
        self.lobby_state = state
