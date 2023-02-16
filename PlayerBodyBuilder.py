import pygame


class PlayerBodyBuilder:
    def __init__(self):
        self.surface = pygame.surface.Surface((64, 64), pygame.SRCALPHA)

    def add_triangle_base(self) -> 'PlayerBodyBuilder':
        triangle_size: int = 10
        triangle = ((0, -triangle_size), (-triangle_size, triangle_size // 2), (triangle_size, triangle_size // 2))
        center_x = self.surface.get_width() // 2
        center_y = self.surface.get_height() // 2
        pygame.draw.polygon(self.surface, (100, 255, 100), [(center_x + t[0], center_y + t[1]) for t in triangle])
        return self

    def build(self) -> 'pygame.surface.Surface':
        return self.surface
