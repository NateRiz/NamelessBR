from collections import defaultdict
from typing import Callable, DefaultDict

from Engine.Actor import Actor
from MessageMapper import MessageMapper
from Networking.Message import Message
from Serializable.InitialSyncResponse import InitialSyncResponse
from Serializable.Movement import Movement


class ClientLogic(Actor):
    """
    Handles incoming messages from the server and dispatches to corresponding function
    """
    def __init__(self):
        super().__init__()
        self.callback_map: DefaultDict[int, Callable[[int, dict, int], None]] = defaultdict(
            lambda: self._unknown)
        self.callback_map.update({
            MessageMapper.INITIAL_SYNC_RESPONSE: self._initial_sync_response,
            MessageMapper.MOVEMENT: self._movement,
        })

    def update(self):
        """
        Gets all queued messages from the server and dispatches them.
        """
        message = self.get_world().network.client.get_next_message()
        while message is not None:
            self._dispatch(message)
            message = self.get_world().network.client.get_next_message()

    def _dispatch(self, message: Message):
        for message_type, msg in message.message.items():
            self._dispatch_one(message_type, msg, message.owner_id)

    def _dispatch_one(self, message_type: int, message: dict, owner: int):
        self.callback_map[message_type](message_type, message, owner)

    def _initial_sync_response(self, _message_type: int, message: dict, _owner: int):
        response = InitialSyncResponse().load(message)
        self.get_world().on_initial_sync_response(response)

    def _movement(self, message_type: int, message: dict, _owner: int):
        response = Movement().load(message)
        self.get_world().players[response.my_id].server_move_to(response.pos, response.direction)

    def _unknown(self, message_type: int, message: dict, owner: int):
        print(F"WARNING: Received message from P[{owner}] with unknown message type: {message_type} {message}")
