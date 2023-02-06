import pygame

from Engine.Actor import Actor
from Engine.DrawLayer import DrawLayer


class HUD(Actor):
    def __init__(self):
        super().__init__()
        self.set_draw_layer(DrawLayer.HUD)

    def draw(self, screen):
        player = self.get_world().get_my_player()
        w, h = screen.get_size()
        buffer = 8
        y = h - 64

        health_height = 12
        pygame.draw.rect(screen, (0, 0, 0), (buffer, y, player.max_health * 4, health_height))
        pygame.draw.rect(screen, (200, 0, 0), (buffer + 1, y + 1, player.health * 4 - 2, health_height - 2))
