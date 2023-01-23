from Networking.Serializable import Serializable
from Serializable.Room import Room


class ChangeRoomsResponse(Serializable):
    """
    Sends surrounding rooms to client once rooms change.
    """
    def __init__(self, room=None):
        self.room = room

    def load(self, room: dict):
        self.room = Room().load(room["room"])
        return self
