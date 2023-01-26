import weakref
from typing import List, Dict
import pygame

from Engine.Debug import debug
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
        for actor in Actor.actors:
            actor.poll_input(event)

    @staticmethod
    def get_pressed_input_all(pressed):
        """
        sends all pressed keys to all actors
        :param pressed: state of all keys
        """
        for actor in Actor.actors:
            actor.get_pressed_input(pressed)

class Actor:
    """
    The base class for all objects created.
    Inheriting from this class gives access to everything else in World.
    Inheriting also subscribes it to update/poll/draw.
    """

    # Every instance that inherits from Actor.
    # Weak ref because we want GC to take care of it if this is the only reference left to it.
    actors = weakref.WeakSet()
    # All drawable objects
    # Indices represent the layer in which we draw to the screen.
    drawable: List[weakref.WeakSet['Actor']] = [weakref.WeakSet() for _ in range(len(DrawLayer))]

    def __init__(self):
        self._draw_layer = DrawLayer.NONE
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
        Game().network.client.send(message)

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

    def update(self):
        """
        Overridable update placeholder
        """
        pass

    def poll_input(self, event):
        """
        Overridable poll placeholder
        """
        pass

    def get_pressed_input(self, pressed):
        """
        Overridable get pressed keys
        """
        pass

    def draw(self, screen):
        """
        Overridable draw placeholder
        """
        pass

    def __del__(self):
        self._destroy()

    def _destroy(self):
        if self in Actor.actors:
            Actor.actors.remove(self)
        if self in Actor.drawable[self._draw_layer]:
            Actor.drawable[self._draw_layer].remove(self)
