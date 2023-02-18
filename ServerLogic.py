from collections import defaultdict
from typing import DefaultDict, Callable

from Engine.Actor import Actor
from MessageMapper import MessageMapper
from Serializable.ChangeRoomsRequest import ChangeRoomsRequest
from Serializable.ChangeRoomsResponse import ChangeRoomsResponse
from Serializable.InitialSyncResponse import InitialSyncResponse
from Serializable.LeaveRoomResponse import LeaveRoomResponse
from Serializable.Movement import Movement
import Serializable
from Serializable.ServerMetricsResponse import ServerMetricsResponse
from Serializable.ShootProjectileRequest import ShootProjectileRequest
from Serializable.ShootProjectileResponse import ShootProjectileResponse
from ServerOwned.Map import Map
from ServerOwned.ServerValidator import ServerValidator


class ServerLogic:
    """
    Handles incoming messages from clients and dispatches to corresponding function
    """
    def __init__(self, server):
        self.server = server
        self.callback_map: DefaultDict[int, Callable[[int, object, int], None]] = defaultdict(
            lambda: self._unknown)
        self.callback_map.update({
            MessageMapper.MOVEMENT: self._movement,
            MessageMapper.INITIAL_SYNC_REQUEST: self._initial_sync_request,
            MessageMapper.CHANGE_ROOMS_REQUEST: self._change_rooms_request,
            MessageMapper.SHOOT_PROJECTILE_REQUEST: self._shoot_projectile,
            MessageMapper.SERVER_METRICS_REQUEST: self._server_metrics
        })
        self.map = Map()

    def on_start(self):
        """
        Immediately called once when the game starts
        """
        clients = list(self.server.clients.keys())
        self.map.generate(clients)

    def update(self):
        """
        Gets all queued messages from clients and dispatches them.
        """
        server = self.server
        if server is None:
            return

        message = server.get_next_message()
        while message is not None:
            self._dispatch(message)
            message = server.get_next_message()
        self.map.update(self.server)

    def _dispatch(self, message):
        for message_type, msg in message.message.items():
            self._dispatch_one(message_type, msg, message.owner_id)

    def _dispatch_one(self, message_type, message, owner):
        self.callback_map[message_type](message_type, message, owner)

    def _initial_sync_request(self, _message_type, _message, owner):
        y, x = self.map.players[owner].map_coordinates
        master_room = self.map.map[y][x]
        serialized = {owner: Serializable.Player.Player(self.map.players[owner].pos)}
        enemies = [e.get_serialized() for e in master_room.enemies.values()]
        self.server.send(
            {MessageMapper.INITIAL_SYNC_RESPONSE: InitialSyncResponse(owner, len(self.map.map)),
             MessageMapper.CHANGE_ROOMS_RESPONSE: ChangeRoomsResponse(master_room.coordinates, serialized, [], enemies)},
            owner)

    def _movement(self, message_type, message: Movement, owner):
        other_players_in_room = self.map.get_players_in_room(owner)
        self.map.move_player_position(owner, message.pos)
        for player in other_players_in_room:
            self.server.send({message_type: message}, player)

    def _change_rooms_request(self, _message_type, message: ChangeRoomsRequest, owner):
        if not ServerValidator.validate_change_rooms(self.map.players[owner].map_coordinates, message.destination):
            return

        # Get players in last room
        last_room_player_ids = self.map.get_players_in_room(owner)
        y, x = self.map.players[owner].map_coordinates
        if not last_room_player_ids:
            self.map.unload_room(y, x)

        # Let them know this player has left
        for player in last_room_player_ids:
            self.server.send({MessageMapper.LEAVE_ROOM_RESPONSE: LeaveRoomResponse(owner)}, player)

        # Change the players room
        self.map.change_player_room(owner, message.destination)
        y, x = self.map.players[owner].map_coordinates
        master_room = self.map.map[y][x]
        all_player_ids = self.map.get_players_in_room(owner) + [owner]
        players = {p: Serializable.Player.Player(self.map.players[p].pos, self.map.players[p].map_coordinates) for p in all_player_ids}
        projectiles = [p.get_serialized() for p in master_room.projectiles]
        enemies = [e.get_serialized() for e in master_room.enemies.values()]
        for player in all_player_ids:
            self.server.send({MessageMapper.CHANGE_ROOMS_RESPONSE: ChangeRoomsResponse(
                master_room.coordinates, players, projectiles, enemies)}, player)

    def _shoot_projectile(self, _message_type, message: ShootProjectileRequest, owner):
        id_ = self.map.add_projectile(owner, message)

        all_players_in_room = self.map.get_players_in_room(owner) + [owner]
        for player in all_players_in_room:
            self.server.send({MessageMapper.SHOOT_PROJECTILE_RESPONSE: ShootProjectileResponse(id_, message.position, message.direction)}, player)

    def _server_metrics(self, _message_type, _message, owner):
        self.server.send({MessageMapper.SERVER_METRICS_RESPONSE: ServerMetricsResponse(len(Actor.actors))}, owner)

    def _unknown(self, message_type, message, owner):
        print(F"WARNING: Received message from P[{owner}] with unknown message type: {message_type} {message}")
