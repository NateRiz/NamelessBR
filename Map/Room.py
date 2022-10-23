import pygame

from Engine.Actor import Actor


class Room(Actor):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.width = 2500
        self.height = 1500
        self.surface = pygame.Surface((self.width, self.height))

    def draw(self, screen):
        background_color = (45, 45, 45)
        self.surface.fill(background_color)

        dividers = 100
        for i in range(self.height // dividers):
            pygame.draw.rect(self.surface, (80, 80, 80), (0, i * dividers, self.width, 2))
        for i in range(self.width // dividers):
            pygame.draw.rect(self.surface, (80, 80, 80), (i * dividers, 0, 2, self.height))
        pygame.draw.rect(self.surface, (0,249,255), (0, 0, self.width, self.height), 1)

        self.get_screen().blit(self.surface, self.player.offset_position)
