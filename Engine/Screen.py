import pygame

from Engine.Singleton import Singleton


class Screen(metaclass=Singleton):
    def __init__(self):
        self.screen = pygame.display.set_mode((1920, 1080))
