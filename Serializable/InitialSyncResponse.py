from Networking.Serializable import Serializable


class InitialSyncResponse(Serializable):
    """
    Syncs parameters at the start of the game for everyone.
    """
    def __init__(self, players=None, my_id=-1, map_size=None):
        if players is None:
            players = []
        self.players = players
        self.my_id = my_id
        self.map_size = map_size
