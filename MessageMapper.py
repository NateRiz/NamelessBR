from enum import IntEnum


class MessageMapper(IntEnum):
    """
    Different message types to be sent over the socket
    """
    NONE = 0
    LIST_CLIENTS_REQUEST = 1
    LIST_CLIENTS_RESPONSE = 2
    MOVEMENT = 3
    START = 4
    INITIAL_SYNC_REQUEST = 5
    INITIAL_SYNC_RESPONSE = 6
    CHANGE_ROOMS_RESPONSE = 7
    CHANGE_ROOMS_REQUEST = 8
    LEAVE_ROOM_RESPONSE = 9
