from Networking.Serializable import Serializable


class ChangeRoomsResponse(Serializable):
    """
    Contains information on how to build a room for the client once they switch to a new room.
    """
    def __init__(self, room_coordinates=None, players=None):
        self.room_coordinates = room_coordinates
        self.players = players
