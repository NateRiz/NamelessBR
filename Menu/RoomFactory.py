import Map


class RoomFactory:
    @staticmethod
    def create(coordinates: list) -> Map.Room.Room:
        room = Map.Room.Room(coordinates)
        room.add_doors()
        return room
