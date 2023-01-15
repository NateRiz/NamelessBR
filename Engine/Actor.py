import weakref
from typing import List
import pygame

from Engine.Debug import debug
from Engine.Game import Game
from Engine.Layer import Layer
from Engine.Screen import Screen


class ActorManager:
    @staticmethod
    def static_init_actor():
        Actor.drawable = [weakref.WeakSet() for _ in range(len(Layer))]

    @staticmethod
    def draw_all():
        for layer in Actor.drawable:
            for actor in layer:
                actor.draw(Screen().screen)
                ActorManager._draw_collision_if_debug(actor)

    @staticmethod
    def update_all():
        for actor in Actor.actors:
            actor.update()

    @staticmethod
    def poll_input_all(event):
        for actor in Actor.actors:
            actor.poll_input(event)

    @staticmethod
    @debug
    def _draw_collision_if_debug(actor):
        if hasattr(actor, "rect"):
            pygame.draw.rect(actor.get_screen(), (0, 255, 255), actor.rect, 1)


class Actor:
    actors = weakref.WeakSet()
    drawable: List[weakref.WeakSet] = list()

    def __init__(self):
        self._draw_layer = Layer.NONE
        Actor.actors.add(self)
        Actor.drawable[Layer.NONE].add(self)

    def destroy(self):
        if self in self.actors:
            self.actors.remove(self)
        if self in Actor.drawable[self._draw_layer]:
            Actor.drawable[self._draw_layer].remove(self)

    def get_world(self):
        return Game().world

    def get_screen(self):
        return Screen().screen

    def send_to_server(self, message: dict):
        return Game().network.client.send(message)

    def set_draw_layer(self, layer):
        if self in Actor.drawable[self._draw_layer]:
            Actor.drawable[self._draw_layer].remove(self)
        self._draw_layer = layer
        Actor.drawable[self._draw_layer].add(self)

    def update(self):
        pass

    def poll_input(self, event):
        pass

    def draw(self, screen):
        pass

    def __del__(self):
        self.destroy()
