from collections import defaultdict
from typing import DefaultDict, Callable

from Engine.Actor import Actor
from Map.MapGenerator import MapGenerator
from MessageMapper import MessageMapper
from Serializable.ChangeRoomsRequest import ChangeRoomsRequest
from Serializable.ChangeRoomsResponse import ChangeRoomsResponse
from Serializable.InitialSyncResponse import InitialSyncResponse
from Serializable.Room import Room
from ServerOwned.Map import Map


class ServerLogic(Actor):
    """
    Handles incoming messages from clients and dispatches to corresponding function
    """

    def __init__(self):
        super().__init__()
        self.callback_map: DefaultDict[int, Callable[[int, dict, int], None]] = defaultdict(
            lambda: self._unknown)
        self.callback_map.update({
            MessageMapper.MOVEMENT: self._movement,
            MessageMapper.INITIAL_SYNC_REQUEST: self._initial_sync_request,
            MessageMapper.CHANGE_ROOMS_REQUEST: self._change_rooms_request,
        })
        self.map = Map()

    def update(self):
        """
        Gets all queued messages from clients and dispatches them.
        """
        server = self.get_world().network.server
        if server is None:
            return

        message = server.get_next_message()
        while message is not None:
            self._dispatch(message)
            message = server.get_next_message()

    def _dispatch(self, message):
        for message_type, msg in message.message.items():
            self._dispatch_one(message_type, msg, message.owner_id)

    def _dispatch_one(self, message_type, message, owner):
        self.callback_map[message_type](message_type, message, owner)

    def _initial_sync_request(self, _message_type, _message, owner):
        clients = list(self.get_world().network.server.clients.keys())
        self.map.generate(clients)
        y, x = self.map.player_positions[owner]
        master_room = self.map.map[y][x]
        room = Room(master_room.coordinates)
        self.get_world().network.server.send(
            {MessageMapper.INITIAL_SYNC_RESPONSE: InitialSyncResponse(clients, owner, len(self.map.map)),
             MessageMapper.CHANGE_ROOMS_RESPONSE: ChangeRoomsResponse(room)},
            owner)

    def _movement(self, message_type, message, owner):
        self.get_world().network.server.send_all_except({message_type: message}, owner)

    def _change_rooms_request(self, message_type, message, owner):
        request = ChangeRoomsRequest().load(message)
        self.map.move_player(owner, request.destination)
        y, x = self.map.player_positions[owner]
        master_room = self.map.map[y][x]
        room = Room(master_room.coordinates)
        self.get_world().network.server.send({MessageMapper.CHANGE_ROOMS_RESPONSE: ChangeRoomsResponse(room)}, owner)

    def _unknown(self, message_type, message, owner):
        print(F"WARNING: Received message from P[{owner}] with unknown message type: {message_type} {message}")

    def _get_surrounding_rooms(self, src):
        src_x, src_y = src
        rooms = []
        for y in range(src_y - 1, src_y + 2):
            for x in range(src_x - 1, src_x + 2):
                if src_x == x and src_y == y:
                    continue
                if 0 >= y > len(self.game_map):
                    if 0 >= x > len(self.game_map[y]):
                        rooms.append(self.game_map[y][x])
        return rooms
