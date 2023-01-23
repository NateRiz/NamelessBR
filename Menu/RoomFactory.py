import Serializable
import Map


class RoomFactory:
    @staticmethod
    def create(serialized_room: Serializable.Room.Room) -> Map.Room.Room:
        room = Map.Room.Room(serialized_room.position)
        room.add_doors()
        return room
