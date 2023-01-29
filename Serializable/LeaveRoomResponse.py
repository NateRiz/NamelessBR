from Networking.Serializable import Serializable


class LeaveRoomResponse(Serializable):
    def __init__(self, player_id=None):
        self.player_id = player_id
