import Engine.Actor as Actor


def debug(func):
    """
    Runs the annotated function only if debug mode is enabled
    :param func: Annotated function to be run
    :return: Decorator
    """
    def run_if_debug(*args, **kwargs):
        """
        Runs the annotated function only if debug mode is enabled
        :param args: function args to pass through
        :param kwargs: function kwargs to pass through
        """
        instance: Actor.Actor = args[0]
        if instance.get_world().is_debug:
            func(*args, *kwargs)
    return run_if_debug
