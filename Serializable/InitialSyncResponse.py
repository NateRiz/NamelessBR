from Networking.Serializable import Serializable


class InitialSyncResponse(Serializable):
    def __init__(self, players=None, my_id=-1):
        if players is None:
            players = []
        self.players = players
        self.my_id = my_id