import pygame

from Engine.Actor import Actor
from Engine.Layer import Layer
from Map.Ground import Ground


class Room(Actor):
    def __init__(self, player):
        super().__init__()
        self.set_draw_layer(Layer.ROOM)
        self.player = player
        self.width = 2500
        self.height = 1500
        self.surface = pygame.Surface((self.width, self.height))
        self.ground = Ground(self.surface)

    def draw(self, screen):
        self.get_screen().blit(self.surface, self.player.offset_position)

    def draw_to_room(self, surface, position):
        self.surface.blit(surface, position)

    def get_surface(self):
        return self.surface
