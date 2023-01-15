from Engine.Actor import Actor
from Engine.Game import Game
from MessageMapper import MessageMapper


class ServerLogic(Actor):
    def __init__(self):
        super().__init__()

    def update(self):
        server = Game().network.server
        if server is None:
            return

        message = server.get_next_message()
        while message is not None:
            self.dispatch(message)
            message = server.get_next_message()

    def dispatch(self, message):
        for message_type, msg in message.message.items():
            self._disaptch_one(message_type, msg, message.owner_id)

    def _disaptch_one(self, message_type, message, owner):
        server = Game().network.server
        match message_type:
            case MessageMapper.NONE:
                pass
            case MessageMapper.MOVEMENT:
                server.send_all_except({message_type: message}, owner)
            case _:
                print(f"Message Type not found. Message was: {message}")




