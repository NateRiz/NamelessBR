class Room:
    """
    Master instance of a Room. Contains all information about a room.
    Created by the server and relayed to clients through Serializable/Room
    """
    def __init__(self, coordinates, difficulty):
        self.coordinates = coordinates
        self.difficulty = difficulty
        self.actors = {}
