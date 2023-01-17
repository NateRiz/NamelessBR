from Engine.Singleton import Singleton
from Map.MapGenerator import MapGenerator
from Engine.Screen import Screen
from pygame import locals
import pygame
import sys


class Game(metaclass=Singleton):
    """
    Singleton class that controls top level engine objects and window settings
    """
    def __init__(self, network=None):
        super().__init__()
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.screen = Screen()
        self.map_generator = MapGenerator(1)
        self.world = None
        self.network = network

    def main_loop(self, world):
        """
        starts the main loop of the world
        :param world: World singleton
        """
        self.world = world
        self.world.initial_sync()
        self.map_generator.generate()
        # self.map_generator.draw()

        while 1:
            self._poll_input()
            self._update()
            self._draw()

    def _update(self):
        self.clock.tick(self.fps)
        self.world.update()

    def _poll_input(self):
        for event in pygame.event.get():
            if event.type == locals.QUIT:
                pygame.quit()
                sys.exit()
            self.world.poll_input(event)

    def _draw(self):
        self.screen.screen.fill((20, 20, 20))
        self.world.draw()
        pygame.display.flip()
