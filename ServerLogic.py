from collections import defaultdict

from Engine.Actor import Actor
from MessageMapper import MessageMapper
from Serializable.InitialSyncResponse import InitialSyncResponse


class ServerLogic(Actor):
    """
    Handles incoming messages from clients and dispatches to corresponding function
    """
    def __init__(self):
        super().__init__()
        self.callback_map = defaultdict(lambda: self._unknown)
        self.callback_map.update({
            MessageMapper.MOVEMENT: self._movement,
            MessageMapper.INITIAL_SYNC_REQUEST: self._initial_sync_request
        })

    def update(self):
        server = self.get_world().network.server
        if server is None:
            return

        message = server.get_next_message()
        while message is not None:
            self.dispatch(message)
            message = server.get_next_message()

    def dispatch(self, message):
        for message_type, msg in message.message.items():
            self._dispatch_one(message_type, msg, message.owner_id)

    def _dispatch_one(self, message_type, message, owner):
        self.callback_map[message_type](message_type, message, owner)

    def _initial_sync_request(self, _message_type, _message, owner):
        response = InitialSyncResponse(list(self.get_world().network.server.clients.keys()), owner)
        self.get_world().network.server.send({MessageMapper.INITIAL_SYNC_RESPONSE: response}, owner)

    def _movement(self, message_type, message, owner):
        self.get_world().network.server.send_all_except({message_type: message}, owner)

    def _unknown(self, message_type, message, owner):
        print(F"WARNING: Received message from P[{owner}] with unknown message type: {message_type} {message}")
