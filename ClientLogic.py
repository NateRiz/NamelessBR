from collections import defaultdict
from typing import Callable, DefaultDict

from Engine.Actor import Actor
from MessageMapper import MessageMapper
from Networking.Message import Message
from Serializable.ChangeRoomsResponse import ChangeRoomsResponse
from Serializable.DeleteEnemy import DeleteEnemy
from Serializable.DeleteProjectile import DeleteProjectile
from Serializable.Enemy import Enemy
from Serializable.InitialSyncResponse import InitialSyncResponse
from Serializable.LeaveRoomResponse import LeaveRoomResponse
from Serializable.Movement import Movement
from Serializable.ServerMetricsResponse import ServerMetricsResponse
from Serializable.ShootProjectileResponse import ShootProjectileResponse


class ClientLogic(Actor):
    """
    Handles incoming messages from the server and dispatches to corresponding function
    """

    def __init__(self):
        super().__init__()
        self.callback_map: DefaultDict[int, Callable[[int, object], None]] = defaultdict(
            lambda: self._unknown)
        self.callback_map.update({
            MessageMapper.INITIAL_SYNC_RESPONSE: self._initial_sync_response,
            MessageMapper.MOVEMENT: self._movement,
            MessageMapper.CHANGE_ROOMS_RESPONSE: self._change_rooms_response,
            MessageMapper.LEAVE_ROOM_RESPONSE: self._leave_room_response,
            MessageMapper.SHOOT_PROJECTILE_RESPONSE: self._shoot_projectile_response,
            MessageMapper.SERVER_METRICS_RESPONSE: self._server_metrics,
            MessageMapper.UPDATE_ENEMY: self._update_enemy,
            MessageMapper.DELETE_PROJECTILE: self._delete_projectile,
            MessageMapper.DELETE_ENEMY: self._delete_enemy,
        })

    def update(self):
        """
        Gets all queued messages from the server and dispatches them.
        """
        message = self.get_world().client.get_next_message()
        while message is not None:
            self._dispatch(message)
            message = self.get_world().client.get_next_message()

    def _dispatch(self, message: Message):
        for message_type, msg in message.message.items():
            self._dispatch_one(message_type, msg, message.owner_id)

    def _dispatch_one(self, message_type: int, message: object, _owner: int):
        self.callback_map[message_type](message_type, message)

    def _initial_sync_response(self, _message_type: int, message: InitialSyncResponse):
        self.get_world().on_initial_sync_response(message)

    def _movement(self, _message_type: int, message: Movement):
        if message.my_id not in self.get_world().room.players:
            print(f"Player {message.my_id} not in my room yet. Tried to move")
            return
        self.get_world().room.players[message.my_id].server_move_to(message.pos, message.direction, message.angle)

    def _change_rooms_response(self, _message_type: int, message: ChangeRoomsResponse):
        self.get_world().update_room(message)

    def _leave_room_response(self, _message_type: int, message: LeaveRoomResponse):
        self.get_world().room.try_remove_player(message.player_id)

    def _shoot_projectile_response(self, _message_type: int, message: ShootProjectileResponse):
        self.get_world().room.spawn_projectile(message.position, message.direction)

    def _update_enemy(self, _message_type: int, message: Enemy):
        room = self.get_world().room
        if not room:
            return
        self.get_world().room.update_enemy(message)

    def _delete_projectile(self, _message_type: int, message: DeleteProjectile):
        self.get_world().room.remove_projectile(message.my_id)

    def _delete_enemy(self, _message_type: int, message: DeleteEnemy):
        self.get_world().room.remove_enemy(message.my_id)

    def _server_metrics(self, _message_type: int, message: ServerMetricsResponse):
        self.get_world().debugger.set_server_metrics(message)

    def _unknown(self, message_type: int, message: dict):
        print(F"WARNING: Received message from [Server] with unknown message type: {message_type} {message}")
