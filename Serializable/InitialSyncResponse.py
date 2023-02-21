class InitialSyncResponse:
    """
    Syncs parameters at the start of the game for everyone.
    """
    def __init__(self, my_id, map_size):
        self.my_id = my_id
        self.map_size = map_size
