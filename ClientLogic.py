from collections import defaultdict

from Engine.Actor import Actor
from MessageMapper import MessageMapper
from Serializable.InitialSyncResponse import InitialSyncResponse
from Serializable.Movement import Movement


class ClientLogic(Actor):
    def __init__(self):
        super().__init__()
        self.callback_map = defaultdict(lambda: self._unknown)
        self.callback_map.update({
            MessageMapper.INITIAL_SYNC_RESPONSE: self._initial_sync_response,
            MessageMapper.MOVEMENT: self._movement,
        })

    def update(self):
        message = self.get_world().network.client.get_next_message()
        while message is not None:
            self.dispatch(message)
            message = self.get_world().network.client.get_next_message()

    def dispatch(self, message):
        for message_type, msg in message.message.items():
            self._dispatch_one(message_type, msg, message.owner_id)

    def _dispatch_one(self, message_type, message, owner):
        self.callback_map[message_type](message_type, message, owner)

    def _initial_sync_response(self, _message_type, message, _owner):
        response = InitialSyncResponse().load(message)
        self.get_world().on_initial_sync_response(response)

    def _movement(self, _message_type, message, _owner):
        response = Movement().load(message)
        self.get_world().players[response.my_id].server_move_to(response.pos, response.direction)

    def _unknown(self, message_type, message, owner):
        print(F"WARNING: Received message from P[{owner}] with unknown message type: {message_type} {message}")
