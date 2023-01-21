import pygame

from Engine.Actor import Actor
from Engine.Layer import Layer


class Door(Actor):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def __init__(self, surface, direction):
        super().__init__()
        self.set_draw_layer(Layer.STRUCTURE)
        self.surface = surface
        self.direction = direction
        self.width = 80
        self.height = 10
        room_w, room_h = self.surface.get_size()
        self.rect = {
            Door.NORTH: pygame.rect.Rect(room_w // 2 - self.width // 2, 0, self.width, self.height),
            Door.SOUTH: pygame.rect.Rect(room_w // 2 - self.width // 2, room_h - self.height, self.width, self.height),
            Door.WEST: pygame.rect.Rect(0, room_h // 2 - self.width // 2, self.height, self.width),
            Door.EAST: pygame.rect.Rect(room_w - self.height, room_h // 2 - self.width // 2, self.height, self.width)
        }[self.direction]

    def update(self):
        player = self.get_world().get_my_player()
        if not player:
            return
        if self.rect.colliderect(player.rect):
            print("collide")

    def draw(self, screen):
        self._draw_doors()

    def _draw_doors(self):
        pygame.draw.rect(self.surface, (200, 200, 200), self.rect)
