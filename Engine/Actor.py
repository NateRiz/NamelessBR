import weakref
from typing import List, Dict

from Engine.CollisionLayer import CollisionLayer
from Engine.Game import Game
from Engine.DrawLayer import DrawLayer
from Engine.Screen import Screen
from Networking.Serializable import Serializable


class ActorManager:
    """
    Manager for all actors
    """
    @staticmethod
    def draw_all():
        """
        Call the draw function on all actors in sorted increasing order
        """
        for layer in Actor.drawable:
            for actor in layer:
                actor.draw(Screen().screen)

    @staticmethod
    def update_all():
        """
        Call the update function on all actors
        """
        actors_to_update = list(Actor.actors)
        for actor in actors_to_update:
            actor.update()

    @staticmethod
    def poll_input_all(event):
        """
        sends one poll event to all actors
        """
        actors_to_update = list(Actor.actors)
        for actor in actors_to_update:
            actor.poll_input(event)

    @staticmethod
    def get_pressed_input_all(pressed):
        """
        sends all pressed keys to all actors
        :param pressed: state of all keys
        """
        actors_to_update = list(Actor.actors)
        for actor in actors_to_update:
            actor.get_pressed_input(pressed)

    @staticmethod
    def check_collisions_all():
        """Checks for collisions for all objects that have a collision mask"""
        for actor in Actor.actors:
            actor.check_collisions()

    @staticmethod
    def clean_all():
        Actor.actors = set(filter(lambda a: not a._is_marked_for_deletion, Actor.actors))




class Actor:
    """
    The base class for all objects created.
    Inheriting from this class gives access to everything else in World.
    Inheriting also subscribes it to update/poll/draw.
    """

    # Every instance that inherits from Actor. This is the only container that contains true references in this program.
    # Everything else that creates an actor creates a weakref proxy that is ignored by garbage collection. Ensure that
    # an actor is not used after its freed.
    actors = set()
    # All drawable objects
    # Indices represent the layer in which we draw to the screen.
    drawable: List[weakref.WeakSet['Actor']] = [weakref.WeakSet() for _ in range(len(DrawLayer))]
    # All objects that can be collided with
    # Indices represent the layer in which the object resides
    collidable: List[weakref.WeakSet['Actor']] = [weakref.WeakSet() for _ in range(len(CollisionLayer))]

    @classmethod
    def new(cls, *args, **kwargs):
        """
        The factory method for creating actors. init is disabled for actors. References are stored in the static actors
        set. Everything else uses weakrefs which is ignored by gc.
        :param args: init args
        :param kwargs: init kwargs
        :return: weakref to new object
        """
        obj = super().__new__(cls)
        obj.__init__(*args, **kwargs)
        return weakref.proxy(obj)

    def add_child(self, obj):
        """
        Adds a child actor. All children are automatically freed when this object is freed.
        :param obj: Child actor
        :return: passed in obj
        """
        self.children.append(obj)
        return self.children[-1]

    def __new__(*args, **kwargs):
        raise Exception("Actors cannot be directly initialized. Use: Actor.new()")

    def free(self):
        """
        Mark the object for deletion. The reference will be removed during the ActorManager.clean_all stage.
        Recursively free children objects.
        """
        self._is_marked_for_deletion = True
        for child in self.children:
            child.free()

    def __init__(self):
        self.children = []
        self._is_marked_for_deletion = False
        self._draw_layer = DrawLayer.NONE
        # Collision mask is the collision layer that this object scans to collide with
        self._collision_masks: set[int] = set()
        self._collision_layer = CollisionLayer.NONE
        Actor.actors.add(self)
        Actor.drawable[DrawLayer.NONE].add(self)

    def get_world(self):
        """
        Get the world singleton
        :return: World singleton
        """
        return Game().world

    def get_screen(self):
        """
        Get the pygame screen
        :return: Screen singleton
        """
        return Screen().screen

    def send_to_server(self, message: Dict[int, Serializable]):
        """
        Send a message to the server
        :param message: Message to send to server
        """
        Game().client.send(message)

    def set_draw_layer(self, layer):
        """
        Sets the layer for an object to be drawn
        Layers are drawn in increasing order [0...n]
        :param layer: layer to draw object on
        """
        if self in Actor.drawable[self._draw_layer]:
            Actor.drawable[self._draw_layer].remove(self)
        self._draw_layer = layer
        Actor.drawable[self._draw_layer].add(self)

    def set_collision_layer(self, layer):
        assert layer != CollisionLayer.NONE, "There is no reason to set collision layer to none"
        assert self._collision_layer == CollisionLayer.NONE, "No support for changing collision layers, yet."
        self._collision_layer = layer
        self.collidable[layer].add(self)

    def add_collision_mask(self, mask):
        self._collision_masks.add(mask)

    def update(self):
        """Overridable update placeholder"""
        pass

    def poll_input(self, event):
        """Overridable poll placeholder"""
        pass

    def get_pressed_input(self, pressed):
        """Overridable get pressed keys"""
        pass

    def draw(self, screen):
        """Overridable draw placeholder"""
        pass

    def on_collide(self, actor: "Actor"):
        """
        Overridable collide placeholder. Called when an object in this object's masks collides with its rect
        :param actor: Actor collided with
        """
        pass

    def __del__(self):
        self._destroy()

    def check_collisions(self):
        for mask in self._collision_masks:
            for actor in Actor.collidable[mask]:
                if self.rect.colliderect(actor.rect):
                    self.on_collide(actor)


    def _destroy(self):
        if self in Actor.drawable[self._draw_layer]:
            Actor.drawable[self._draw_layer].remove(self)
