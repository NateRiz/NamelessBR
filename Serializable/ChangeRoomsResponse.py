from Networking.Serializable import Serializable
from Serializable.Player import Player


class ChangeRoomsResponse(Serializable):
    """
    Contains information on how to build a room for the client once they switch to a new room.
    """

    def __init__(self, room_coordinates=None, players: dict[int:Player] | None = None):
        self.room_coordinates = room_coordinates
        self.players = players

    def load(self, obj: dict):
        """
        Update the instance using the retrieved json dict
        :param obj: dict to update instance
        :return: self
        """
        object_vars = len(obj)
        self.__dict__.update(obj)
        self.players = {int(id_): Player().load(player) for id_, player in self.players.items()}
        assert object_vars == len(vars(
            self)), f"Object has gained unexpected class attributes: Found {vars(self)}. Expected only {object_vars}"
        return self
