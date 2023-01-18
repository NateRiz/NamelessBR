import pygame
import os
import psutil

from Engine.Actor import Actor
from Engine.Debug import debug
from Engine.Layer import Layer


class Debugger(Actor):
    """
    Debugger panel with relative metrics. Default mapped to F12 once the game starts.
    """
    def __init__(self):
        super().__init__()
        self.set_draw_layer(Layer.DEBUG)
        self.font = pygame.font.Font(pygame.font.get_default_font(), 16)
        self.server_kb = 0
        self.metrics = {"Debugger": ""}

    @debug
    def update(self):
        """
        Updates metrics every frame
        """
        self.metrics["Player Id"] = self.get_world().my_id
        self.metrics["Server Incoming"] = F"{self._get_server_metrics()} KB/s"
        self.metrics["Client Incoming"] = F"{self._get_client_metrics()} KB/s"
        self.metrics["Memory"] = F"{self._get_memory_usage()} MB"
        self.metrics["Actors"] = F"{len(Actor.actors)}"

    @debug
    def draw(self, screen):
        """
        Draws panel and metrics to the screen
        :param screen: Pygame screen to draw on
        """
        panel_size = (400, screen.get_height())
        panel = pygame.surface.Surface(panel_size, pygame.SRCALPHA)
        pygame.draw.rect(panel, (0, 0, 0, 100), pygame.rect.Rect(0, 0, *panel_size))

        for i, (k, v) in enumerate(self.metrics.items()):
            text = self.font.render(F"{k}: {v}", True, (255, 255, 255))
            panel.blit(text, (8, 8 + i * 2 * self.font.get_height()))

        screen.blit(panel, (screen.get_width() - panel_size[0], 0))

    def _get_server_metrics(self):
        server = self.get_world().network.server
        if not server:
            return 0
        return server.get_incoming_kb_metric()

    def _get_client_metrics(self):
        return self.get_world().network.client.get_incoming_kb_metric()

    def _get_memory_usage(self):
        process = psutil.Process(os.getpid())
        return process.memory_info().rss // (1024*1024)
