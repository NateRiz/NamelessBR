class Message:
    """
    Basic form of a packet retrieved from a socket. Later is parsed into an actual object.
    """
    def __init__(self, owner_id: int, message: dict):
        self.owner_id = owner_id
        self.message = {int(msg_type): msg for (msg_type, msg) in message.items()}
