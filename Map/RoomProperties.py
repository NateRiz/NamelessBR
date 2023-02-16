from random import randint

from Enemy.Body.EnemyType import EnemyType
from Map.Room import Room
from Settings import Settings


class RoomProperties:
    def __init__(self):
        self.enemies = set()

    def add_enemy(self, enemy_type: EnemyType):
        buffer = 16
        x = randint(buffer, Settings.ROOM_WIDTH-buffer)
        y = randint(buffer, Settings.ROOM_HEIGHT-buffer)
        self.enemies.add((enemy_type, x, y))

    def update_properties(self, room: Room):
        enemies = [enemy.get_serialized() for enemy in room.enemies.values()]
        self.enemies = set((enemy.enemy_type, *enemy.position) for enemy in enemies)
