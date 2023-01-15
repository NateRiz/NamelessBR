import pygame.rect

from Networking.Network import Network


class PlayerContainer:
    def __init__(self, network, screen_availability):
        self.network: Network = network
        self.containers = {}
        self.screen_availability = screen_availability

    def update(self):
        pass

    def draw(self, screen):
        for rect in self.containers.values():
            pygame.draw.rect(screen, (220, 220, 15), rect, 2, 8)

    def update_players(self, player_ids):
        for i in player_ids:
            self.containers[i] = pygame.rect.Rect(0, 0, 0, 0)
        self._recalculate_bounds()

    def _recalculate_bounds(self):
        x, y, w, h = self.screen_availability
        size = len(self.containers)
        buffer = 16
        container_size = (h - y) // size - buffer
        for i, (k, v) in enumerate(self.containers.items()):
            container_y = y + (buffer + container_size) * i
            self.containers[k] = pygame.rect.Rect(x, container_y, w, container_size)
