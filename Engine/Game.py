from Map.MapGenerator import MapGenerator
from Engine.Screen import Screen
from World import World
from pygame import locals
import pygame
import sys


class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.screen = Screen()
        self.map_generator = MapGenerator(1)
        self.world = World()

    def main_loop(self):
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
