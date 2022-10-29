class MessageMapper:
    NONE = 0
    MOVEMENT = 1

    def __init__(self):
        self.map = {}

    def register(self, key, callback):
        if key in self.map:
            print(f"WARNING: {key} is already registered in the MessageMapper: {callback}")

        self.map[key] = callback


