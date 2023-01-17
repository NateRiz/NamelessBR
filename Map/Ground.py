import pygame

from Engine.Actor import Actor
from Engine.Layer import Layer


class Ground(Actor):
    """
    Bottom ground layer in a room to start drawing.
    """
    def __init__(self, surface):
        super().__init__()
        self.set_draw_layer(Layer.GROUND)
        self.surface = surface

    def draw(self, screen):
        """
        Clears the surface and draws the bottom layer ground.
        :param screen: pygame screen to draw to
        """
        width, height = self.surface.get_size()
        background_color = (45, 45, 45)
        self.surface.fill(background_color)

        dividers = 100
        for i in range(height // dividers):
            pygame.draw.rect(self.surface, (80, 80, 80), (0, i * dividers, width, 2))
        for i in range(width // dividers):
            pygame.draw.rect(self.surface, (80, 80, 80), (i * dividers, 0, 2, height))
        pygame.draw.rect(self.surface, (0, 249, 255), (0, 0, width, height), 1)
