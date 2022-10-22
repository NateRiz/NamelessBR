import Engine.Actor as Actor


def debug(func):
    def run_if_debug(*args, **kwargs):
        instance: Actor.Actor = args[0]
        if instance.get_world().is_debug:
            func(*args, *kwargs)
    return run_if_debug