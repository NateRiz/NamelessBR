import weakref


class Proxy(weakref.ref):
    """
    A proxy class that combines the functionality of weakref.proxy and weakref.ref
    weakref.ref requires using a call operator() to retrieve the original reference or None. (Also is hashable)
    weakref.proxy acts like the original object but there's no way to check if the object is alive.
    This class automatically calls the call operator and forward the result.
    """
    def __init__(self, obj):
        super().__init__(obj)

    def __getattribute__(self, item):
        if item == "is_alive":
            return lambda: self() is not None
        return self().__getattribute__(item)

    def __setattr__(self, key, value):
        return self().__setattr__(key, value)
