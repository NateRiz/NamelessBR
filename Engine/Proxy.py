import weakref
from typing import TypeVar, Generic, Optional

T = TypeVar('T')


class Proxy:
    """
    A proxy class that combines the functionality of weakref.proxy and weakref.ref
    weakref.ref requires using a call operator() to retrieve the original reference or None. (Also is hashable)
    weakref.proxy acts like the original object but there's no way to check if the object is alive.
    This class automatically calls the call operator and forward the result.
    """

    def __init__(self, obj: T) -> None:
        """
        Initializes a new instance of the WeakRef class with the specified object.

        Args:
            obj: The object to wrap with a weak reference.
        """
        self._ref = weakref.ref(obj)
        self._proxy = weakref.proxy(obj)

    def __getattr__(self, name: str) -> Optional[any]:
        """
        Gets the value of the specified attribute from the wrapped object.

        If the wrapped object has been garbage collected, returns None.

        Args:
            name: The name of the attribute to get.

        Returns:
            The value of the attribute from the wrapped object, or None if the object has been garbage collected.
        """
        if name in ['_ref', '_proxy']:
            return super().__getattr__(name)
        if self._ref() is not None:
            return getattr(self._proxy, name)
        return None

    def __setattr__(self, name: str, value: any) -> None:
        """
        Sets the value of the specified attribute on the wrapped object.

        If the wrapped object has been garbage collected, raises an AttributeError.

        Args:
            name: The name of the attribute to set.
            value: The value to set the attribute to.
        """
        if name in ['_ref', '_proxy']:
            super().__setattr__(name, value)
        elif self._ref() is not None:
            setattr(self._proxy, name, value)
        else:
            raise AttributeError(f"Attribute {name} cannot be set because the object has been garbage collected")

    def is_alive(self) -> bool:
        """
        Returns True if the wrapped object is still alive (has not been garbage collected), otherwise False.
        """
        return self._ref() is not None

    def __bool__(self) -> bool:
        """
        Returns True if the wrapped object is still alive (has not been garbage collected), otherwise False.
        """
        return bool(self._ref())
