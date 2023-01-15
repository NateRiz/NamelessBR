class MessageMapper:
    NONE = 0
    SYNC_CLIENTS_REQUEST = 1
    SYNC_CLIENTS_RESPONSE = 2
    MOVEMENT = 3


    def __init__(self):
        self.map = {}

    def register(self, key, callback):
        if key in self.map:
            print(f"WARNING: {key} is already registered in the MessageMapper: {callback}")

        self.map[key] = callback


