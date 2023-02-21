from enum import IntEnum

import Engine.Actor as Actor


def debug(func):
    """
    Runs the annotated function only if debug mode is enabled
    :param func: Annotated function to be run
    :return: Decorator
    """

    def _run_if_debug(*args, **kwargs):
        instance: Actor.Actor = args[0]
        if instance.get_world().is_debug:
            func(*args, *kwargs)

    return _run_if_debug


class DebugShape(IntEnum):
    RECTANGLE = 0
    CIRCLE = 1


def debug_draw(color, shape=DebugShape.RECTANGLE):
    """
    Tags the function with a color for telling the debugger to draw it
    Functions are objects, so they can be given data
    :param color: Color to draw the object
    :param shape: Shape of the object
    :return: Decorator
    """

    def _debug_draw(func):
        func._debug = color
        func._debug_shape = shape
        return func

    return _debug_draw
