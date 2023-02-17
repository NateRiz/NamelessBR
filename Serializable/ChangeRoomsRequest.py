class ChangeRoomsRequest:
    """
    Request from a client to switch to a different room
    """

    def __init__(self, destination=(-1, -1)):
        self.destination = destination
