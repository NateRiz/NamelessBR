from Map.MapGenerator import MapGenerator
from ServerOwned.Player import Player
from ServerOwned.Room import Room


class Map:
    def __init__(self):
        self.map: list[list[Room]] = []
        self.end_position = []  # End room coordinate in map
        self.players: dict[int, Player] = {}  # Server owned player object

    def generate(self, player_ids):
        if self.map:
            # Already has been generated.
            return
        map_generator = MapGenerator(player_ids)
        map_generator.generate()
        map_generator.debug_draw_map()
        self.map = map_generator.map
        self.end_position = map_generator.end_room
        self.players = {id_: Player((800, 500), map_generator.players[id_]) for id_ in player_ids}
        for id_, p in self.players.items():
            y, x = p.map_coordinates
            self.map[y][x].players[id_] = p

    def change_player_room(self, player_id, destination):
        src = self.players[player_id].map_coordinates
        # Copy the player into the next room
        self.map[destination[0]][destination[1]].players[player_id] = self.players[player_id]
        # Remove from the previous room
        del self.map[src[0]][src[1]].players[player_id]
        # Update player map coordinates
        self.players[player_id].map_coordinates = tuple(destination)

    def move_player_position(self, player_id, position):
        """
        Update the players position inside the room
        :param player_id: Player id to update
        :param position: position relative to the room
        """
        self.players[player_id].position = position

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
