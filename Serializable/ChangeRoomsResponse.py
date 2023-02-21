from Serializable.Enemy import Enemy
from Serializable.Player import Player
from Serializable.Projectile import Projectile


class ChangeRoomsResponse:
    """
    Contains information on how to build a room for the client once they switch to a new room.
    """

    def __init__(self, room_coordinates, players: dict[int, Player], projectiles: list[Projectile],
                 enemies: list[Enemy]):
        self.room_coordinates = room_coordinates
        self.players = players
        self.projectiles = projectiles
        self.enemies = enemies
