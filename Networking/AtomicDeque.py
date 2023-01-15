from collections import deque


# Wrapper class that only allows for atomic operations
class AtomicDeque:
    def __init__(self):
        self._deque = deque()

    def append(self, __x) -> None:
        """ Socket will append"""
        return self._deque.append(__x)

    def appendleft(self, __x) -> None:
        """Extra section of packet will be pushed back to the top"""
        return self._deque.appendleft(__x)

    def pop(self):
        """Unused"""
        return self._deque.pop()

    def popleft(self):
        """Receive a message"""
        return self._deque.popleft()

    def __len__(self):
        return len(self._deque)

    def __str__(self):
        return str(self._deque)

    def __repr__(self):
        return repr(self._deque)

