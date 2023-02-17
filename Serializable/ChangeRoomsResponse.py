from Serializable.Enemy import Enemy
from Serializable.Player import Player
from Serializable.Projectile import Projectile


class ChangeRoomsResponse:
    """
    Contains information on how to build a room for the client once they switch to a new room.
    """

    def __init__(self, room_coordinates=None, players: dict[int:Player] | None = None, projectiles: list[Projectile]=None, enemies: list[Enemy]=None):
        self.room_coordinates = room_coordinates
        self.players = players
        self.projectiles = projectiles
        self.enemies = enemies

    def load(self, obj: dict):
        """
        Update the instance using the retrieved json dict
        :param obj: dict to update instance
        :return: self
        """
        object_vars = len(obj)
        self.__dict__.update(obj)
        self.players = {int(id_): Player().load(player) for id_, player in self.players.items()}
        self.projectiles = [Projectile().load(projectile) for projectile in self.projectiles]
        self.enemies = [Enemy().load(enemy) for enemy in self.enemies]
        assert object_vars == len(vars(
            self)), f"Object has gained unexpected class attributes: Found {vars(self)}. Expected only {object_vars}"
        return self
