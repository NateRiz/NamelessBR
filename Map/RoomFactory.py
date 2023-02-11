from Map.Room import Room
from Map.RoomProperties import RoomProperties
from Projectile.Projectile import Projectile
from Projectile.Simple import Simple
from Serializable.ChangeRoomsResponse import ChangeRoomsResponse


class RoomFactory:
    @staticmethod
    def create(coordinates: list) -> Room:
        room = Room.new(coordinates)
        room.add_doors()
        room.add_walls()
        return room

    @staticmethod
    def update_with_room_properties(room: Room, room_properties: RoomProperties):
        for enemy in room_properties.enemies:
            enemy_type, x, y = enemy
            room.spawn_enemy(enemy_type, x, y)

    @staticmethod
    def update_with_change_room_response(room: Room, change_rooms_response: ChangeRoomsResponse):
        [room.spawn_projectile(Simple.new(p.position, p.direction)) for p in change_rooms_response.projectiles]
        [room.spawn_enemy(e.enemy_type, *e.position) for e in change_rooms_response.enemies]
