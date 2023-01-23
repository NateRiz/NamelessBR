from Map.MapGenerator import MapGenerator


class Map:
    def __init__(self):
        self.map = []
        self.player_positions = {}
        self.end_position = []

    def generate(self, player_ids):
        if self.map:
            # Already has been generated.
            return
        map_generator = MapGenerator(player_ids)
        map_generator.generate()
        map_generator.debug_draw_map()
        self.map = map_generator.map
        self.player_positions = map_generator.players
        self.end_position = map_generator.end_room

    def move_player(self, player_id, destination):
        self.player_positions[player_id] = (destination[0], destination[1])
