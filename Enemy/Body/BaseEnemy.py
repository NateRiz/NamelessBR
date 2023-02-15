from math import sqrt

import pygame

from Enemy.Body.EnemyType import EnemyType
from Engine.Actor import Actor
from Engine.CollisionLayer import CollisionLayer
from Engine.DrawLayer import DrawLayer


class BaseEnemy(Actor):
    def __init__(self):
        super().__init__()
        self.set_collision_layer(CollisionLayer.ENEMY)
        self.enemy_type = EnemyType.NONE
        self.velocity: list = [0, 0]
        self.max_speed: int = 1
        self.acceleration_rate: float = .2
        self.friction: float = 0.2
        self.position = [0, 0]
        self.set_draw_layer(DrawLayer.ENEMY)
        self.surface = pygame.surface.Surface((64, 64), pygame.SRCALPHA)
        self.size = 8
        self.collision_size = 8
        self.max_health = 2
        self.health = self.max_health

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

    def change_health(self, delta):
        self.health += delta

    def draw(self, screen):
        room = self.get_world().room
        if not room:
            return

        center_x = self.surface.get_width() // 2
        center_y = self.surface.get_height() // 2

        health_bar_width = 32
        health_bar_height = 2
        pygame.draw.rect(self.surface, (0, 0, 0), (center_x-health_bar_width//2, 0, health_bar_width+2, health_bar_height+2))
        pygame.draw.rect(self.surface, (255, 0, 0), (center_x-health_bar_width//2+1, 1, int(health_bar_width * (self.health/self.max_health)), health_bar_height))

        room.draw_to_room(self.surface, (self.position[0] - center_x, self.position[1] - center_y))
