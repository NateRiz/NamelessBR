import pygame

from Projectile.Projectile import Projectile


class Simple(Projectile):
    def __init__(self, position, direction):
        super().__init__(position, direction)
        self.speed = 6
        self.size = 5

    @property
    def rect(self):
        return pygame.rect.Rect(*self.position, self.size, self.size)

    def _draw(self, screen):
        surface = self.get_world().room.get_surface()
        pygame.draw.circle(surface, (0, 0, 0), self.position, self.size + 1)
        pygame.draw.circle(surface, (255, 0, 0), self.position, self.size)

    def _update(self):
        self.position[0] += self.speed * self.direction[0]
        self.position[1] += self.speed * self.direction[1]

    def _server_update(self):
        self._update()
