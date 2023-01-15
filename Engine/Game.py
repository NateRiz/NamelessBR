from Engine.Singleton import Singleton
from Map.MapGenerator import MapGenerator
from Engine.Screen import Screen
from pygame import locals
import pygame
import sys


class Game(metaclass=Singleton):
    def __init__(self, network=None):
        super().__init__()
        print(network)
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.screen = Screen()
        self.map_generator = MapGenerator(1)
        self.world = None
        self.network = network

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
        self.get_server_metrics()

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

    def get_server_metrics(self):
        kb = self.network.server.get_incoming_kb_metric()
        if kb:
            print(f'{kb} KB')