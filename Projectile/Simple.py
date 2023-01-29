import pygame

from Engine.DrawLayer import DrawLayer
from Projectile.Projectile import Projectile


class Simple(Projectile):
    def __init__(self, position, direction):
        super().__init__()
        self.set_draw_layer(DrawLayer.PROJECTILE)
        self.position = position
        self.direction = direction
        self.speed = 6
        self.size = 5

    @property
    def rect(self):
        return pygame.rect.Rect(*self.position, self.size, self.size)

    def draw(self, screen):
        surface = self.get_world().room.get_surface()
        pygame.draw.circle(surface, (0, 0, 0), self.position, self.size + 1)
        pygame.draw.circle(surface, (255, 0, 0), self.position, self.size)

    def update(self):
        self.position[0] += self.speed * self.direction[0]
        self.position[1] += self.speed * self.direction[1]
        self.check_collisions()

    def check_collisions(self):
        walls = self.get_world().room.walls
        wall_collisions = [wall.rect for wall in walls]
        if self.rect.collidelist(wall_collisions) != -1:
            self.get_world().room.remove_projectile(self)
