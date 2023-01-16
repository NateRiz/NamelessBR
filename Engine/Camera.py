import pygame

from Engine.Actor import Actor
from Engine.Layer import Layer


class Camera(Actor):
    def __init__(self):
        super().__init__()
        self.set_draw_layer(Layer.DEBUG)
        width = self.get_screen().get_width() // 2
        height = self.get_screen().get_height() // 2
        x = self.get_screen().get_width() // 2 - width // 2
        y = self.get_screen().get_height() // 2 - height // 2
        self.rect = pygame.rect.Rect(x, y, width, height)
