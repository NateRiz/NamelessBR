from math import sqrt

import pygame

from Engine.Actor import Actor
from Engine.DrawLayer import DrawLayer


class BaseEnemy(Actor):
    def __init__(self):
        super().__init__()
        self.velocity: list = [0, 0]
        self.max_speed: int = 1
        self.acceleration_rate: float = .2
        self.friction: float = 0.2
        self.position = [400, 500]
        self.set_draw_layer(DrawLayer.ENEMY)
        self.surface = pygame.surface.Surface((64, 64), pygame.SRCALPHA)
        self.size = 8
        self.collision_size = 6

    @property
    def rect(self):
        return pygame.rect.Rect(self.position[0] - self.collision_size // 2,
                                self.position[1] - self.collision_size // 2, self.collision_size, self.collision_size)

    def move(self, input_):
        normalized_input = [0, 0]
        input_magnitude = sqrt(input_[0] ** 2 + input_[1] ** 2)
        if input_magnitude != 0:
            normalized_input = [input_[0] / input_magnitude, input_[1] / input_magnitude]
        self.velocity[0] = self.velocity[0] + (
                normalized_input[0] * self.acceleration_rate - (self.friction * self.velocity[0]))
        self.velocity[1] = self.velocity[1] + (
                normalized_input[1] * self.acceleration_rate - (self.friction * self.velocity[1]))
        if abs(self.velocity[0]) < .1:
            self.velocity[0] = 0
        if abs(self.velocity[1]) < .1:
            self.velocity[1] = 0

        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

    def draw(self, screen):
        room = self.get_world().room
        if not room:
            return
        room.draw_to_room(self.surface, (
            self.position[0] - self.surface.get_width() // 2, self.position[1] - self.surface.get_height() // 2))
