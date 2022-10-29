from Engine.Singleton import Singleton
from Map.MapGenerator import MapGenerator
from Engine.Screen import Screen
from Network.Client import Client
from pygame import locals
import pygame
import sys


class Game(metaclass=Singleton):
    def __init__(self, server=None):
        super().__init__()
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.screen = Screen()
        self.map_generator = MapGenerator(1)
        self.world = None
        self.server = server
        self.client = Client()

    def main_loop(self, world):
        self.world = world
        self.map_generator.generate()
        # self.map_generator.draw()

        while 1:
            self.poll_input()
            self.update()
            self.draw()

    def update(self):
        self.clock.tick(self.fps)
        self.world.update()

    def poll_input(self):
        for event in pygame.event.get():
            if event.type == locals.QUIT:
                pygame.quit()
                sys.exit()

            self.world.poll_input(event)

    def draw(self):
        self.screen.screen.fill((20, 20, 20))
        self.world.draw()
        pygame.display.flip()
