from collections import defaultdict
from typing import DefaultDict, Callable

from Engine.Actor import Actor
from MessageMapper import MessageMapper
from Serializable.ChangeRoomsRequest import ChangeRoomsRequest
from Serializable.ChangeRoomsResponse import ChangeRoomsResponse
from Serializable.InitialSyncResponse import InitialSyncResponse
from Serializable.Movement import Movement
import Serializable
from ServerOwned.Map import Map
from ServerOwned.ServerValidator import ServerValidator


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

    def on_start(self):
        """
        Immediately called once when the game starts
        """
        clients = list(self.get_world().network.server.clients.keys())
        self.map.generate(clients)

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
        y, x = self.map.players[owner].map_coordinates
        master_room = self.map.map[y][x]
        serialized = {owner: Serializable.Player.Player(self.map.players[owner].position)}
        self.get_world().network.server.send(
            {MessageMapper.INITIAL_SYNC_RESPONSE: InitialSyncResponse(owner, len(self.map.map)),
             MessageMapper.CHANGE_ROOMS_RESPONSE: ChangeRoomsResponse(master_room.coordinates, serialized)},
            owner)

    def _movement(self, message_type, message, owner):
        other_players_in_room = self.map.get_players_in_room(owner)
        request = Movement().load(message)
        self.map.move_player_position(owner, request.pos)
        for player in other_players_in_room:
            self.get_world().network.server.send({message_type: message}, player)

    def _change_rooms_request(self, _message_type, message, owner):
        request = ChangeRoomsRequest().load(message)
        if not ServerValidator.validate_change_rooms(self.map.players[owner].map_coordinates, request.destination):
            return

        self.map.change_player_room(owner, request.destination)
        y, x = self.map.players[owner].map_coordinates
        master_room = self.map.map[y][x]
        all_player_ids = self.map.get_players_in_room(owner) + [owner]
        players = {p: Serializable.Player.Player(self.map.players[p].position) for p in all_player_ids}
        for player in all_player_ids:
            self.get_world().network.server.send({MessageMapper.CHANGE_ROOMS_RESPONSE: ChangeRoomsResponse(
                master_room.coordinates, players)}, player)

    def _unknown(self, message_type, message, owner):
        print(F"WARNING: Received message from P[{owner}] with unknown message type: {message_type} {message}")
