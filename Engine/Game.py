from Engine.Singleton import Singleton
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
        self.MAX_FPS = 60
        self.screen = Screen()
        self.world = None
        self.network = network

    def main_loop(self, world):
        """
        starts the main loop of the world
        :param world: World singleton
        """
        self.world = world
        self.world.on_start()

        while 1:
            self._poll_input()
            self._update()
            self._draw()

    def _update(self):
        self.clock.tick(self.MAX_FPS)
        self.world.update()

    def _poll_input(self):
        for event in pygame.event.get():
            if event.type == locals.QUIT:
                pygame.quit()
                sys.exit()
            self.world.poll_input(event)
        self.world.get_pressed_input(pygame.key.get_pressed())

    def _draw(self):
        self.screen.screen.fill((20, 20, 20))
        self.world.draw()
        pygame.display.flip()
