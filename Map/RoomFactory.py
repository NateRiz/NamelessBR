from Map.Room import Room


class RoomFactory:
    @staticmethod
    def create(coordinates: list, map_size) -> Room:
        room = Room(coordinates)
        room.add_doors(map_size)
        room.add_walls()
        return room
