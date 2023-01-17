from Networking.Serializable import Serializable


class InitialSyncResponse(Serializable):
    """
    Syncs parameters at the start of the game for everyone.
    """
    def __init__(self, players=None, my_id=-1):
        if players is None:
            players = []
        self.players = players
        self.my_id = my_id
