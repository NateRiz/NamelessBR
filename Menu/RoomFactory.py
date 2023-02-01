from Map.Room import Room


class RoomFactory:
    @staticmethod
    def create(coordinates: list) -> Room:
        room = Room(coordinates)
        room.add_doors()
        room.add_walls()
        return room
