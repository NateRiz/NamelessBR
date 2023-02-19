from Engine.Actor import ActorManager, Actor
from Map.MapGenerator import MapGenerator
from Map.Room import Room
from Map.RoomFactory import RoomFactory
from MessageMapper import MessageMapper
from Player import Player
from Projectile.Simple import Simple
from Serializable.DeleteEnemy import DeleteEnemy
from Serializable.DeleteProjectile import DeleteProjectile
from Serializable.Empty import Empty
from Serializable.ShootProjectileRequest import ShootProjectileRequest


class Map:
    def __init__(self):
        self.map: list[list[Room]] = []
        self.map_properties = []
        self.end_position = []  # End room coordinate in map
        self.players: dict[int, Player] = {}  # Server owned player object
        self.map_size = 30

    def update(self, server):
        ActorManager.server_update_all()
        ActorManager.check_collisions_all()
        self._send_deltas(server)
        ActorManager.clean_all()

    def _send_deltas(self, server):
        for room in Actor.find_objects_by_type(Room):  # type: Room
            player_ids = [player_id for player_id in room.players.keys()]
            remaining_enemies = {}
            for id_, enemy in room.enemies.items():
                if enemy.is_alive():
                    remaining_enemies[id_] = enemy
                    enemy_update = enemy.get_serialized_deltas()
                    if enemy_update is None:
                        continue
                    for player_id in player_ids:
                        server.send({MessageMapper.UPDATE_ENEMY: enemy_update}, player_id)
                else:
                    for player_id in player_ids:
                        server.send({MessageMapper.DELETE_ENEMY: DeleteEnemy(id_)}, player_id)
            room.enemies = remaining_enemies
            remaining_projectiles = {}
            for id_, proj in room.projectiles.items():
                if proj.is_alive():
                    remaining_projectiles[id_] = proj
                else:
                    for player_id in player_ids:
                        server.send({MessageMapper.DELETE_PROJECTILE: DeleteProjectile(id_)}, player_id)
            room.projectiles = remaining_projectiles


    def generate(self, player_ids):
        if self.map:
            # Already has been generated.
            return
        map_generator = MapGenerator(player_ids, self.map_size)
        map_generator.generate()
        # map_generator._debug_draw_map()
        self.map = map_generator.map
        self.map_properties = map_generator.map_properties
        self.end_position = map_generator.end_room

        for id_ in player_ids:
            player = Player.new(id_, False)
            player.map_coordinates = map_generator.players[id_]
            self.load_room(*player.map_coordinates)
            self.players[id_] = player
            y, x = player.map_coordinates
            self.map[y][x].players[id_] = player

    def load_room(self, y, x):
        if self.map[y][x] is not None:
            return
        self.map[y][x] = RoomFactory.create([y, x])
        RoomFactory.update_with_room_properties(self.map[y][x], self.map_properties[y][x])

    def unload_room(self, y: int, x: int):
        room = self.map[y][x]
        self.map_properties[y][x].update_properties(room)
        self.map[y][x] = None
        room.free()

    def change_player_room(self, player_id, destination):
        y, x = destination
        # Copy the player into the next room
        self.load_room(y, x)
        self.map[y][x].players[player_id] = self.players[player_id]
        # Update player map coordinates
        self.players[player_id].map_coordinates = tuple(destination)

    def move_player_position(self, player_id, position):
        """
        Update the players position inside the room
        :param player_id: Player id to update
        :param position: position relative to the room
        """
        self.players[player_id].pos = position

    def get_players_in_room(self, player_id) -> list[int]:
        """
        Gets a list of the other players in the same room as the given player. Excluding the given player
        :param player_id: player whose room we're taking from
        :return: list of other players in the same room
        """
        coordinate = self.players[player_id].map_coordinates
        players_in_room = filter(
            lambda id_: id_ != player_id and tuple(self.players[id_].map_coordinates) == tuple(coordinate),
            self.players.keys())
        return list(players_in_room)

    def add_projectile(self, player_id: int, shoot_projectile: ShootProjectileRequest):
        y, x = self.players[player_id].map_coordinates
        room = self.map[y][x]
        return room.spawn_projectile(shoot_projectile.position, shoot_projectile.direction).my_id
