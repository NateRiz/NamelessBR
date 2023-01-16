import pygame
import os
import psutil

from Engine.Actor import Actor
from Engine.Debug import debug
from Engine.Layer import Layer


class Debugger(Actor):
    def __init__(self):
        super().__init__()
        self.set_draw_layer(Layer.DEBUG)
        self.font = pygame.font.Font(pygame.font.get_default_font(), 16)
        self.server_kb = 0
        self.metrics = {"Debugger": ""}

    @debug
    def update(self):
        self.metrics["Player Id"] = self.get_world().my_id
        self.metrics["Server Incoming"] = F"{self.get_server_metrics()} KB/s"
        self.metrics["Memory"] = F"{self.get_memory_usage()} MB"

    @debug
    def draw(self, screen):
        panel_size = (400, screen.get_height())
        panel = pygame.surface.Surface(panel_size, pygame.SRCALPHA)
        pygame.draw.rect(panel, (0, 0, 0, 100), pygame.rect.Rect(0, 0, *panel_size))

        for i, (k, v) in enumerate(self.metrics.items()):
            text = self.font.render(F"{k}: {v}", True, (255, 255, 255))
            panel.blit(text, (8, 8 + i * 2 * self.font.get_height()))

        screen.blit(panel, (screen.get_width() - panel_size[0], 0))

    def get_server_metrics(self):
        server = self.get_world().network.server
        if not server:
            return 0
        return server.get_incoming_kb_metric()

    def get_memory_usage(self):
        process = psutil.Process(os.getpid())
        return process.memory_info().rss // (1024*1024)
