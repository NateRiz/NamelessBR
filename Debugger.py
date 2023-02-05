from time import time
from collections import Counter
import pygame
import os
import psutil

from Engine.Actor import Actor
from Engine.Debug import debug
from Engine.DrawLayer import DrawLayer


class Debugger(Actor):
    """
    Debugger panel with relative metrics. Default mapped to F12 once the game starts.
    """

    def __init__(self):
        super().__init__()
        self.set_draw_layer(DrawLayer.DEBUG)
        self.font = pygame.font.Font(pygame.font.get_default_font(), 16)
        self.metrics = {"Debugger": ""}
        self.fps_incrementer = 0
        self.last_fps = 0
        self.time_since_last_fps_reset = time()

    @debug
    def update(self):
        """
        Updates metrics every frame
        """
        self._update_fps_counter()

        self.metrics["FPS"] = F"{self.last_fps}"
        self.metrics["Player Id"] = self.get_world().my_id
        self.metrics["Client Incoming"] = F"{self._get_client_metrics()} KB/s"
        self.metrics["Memory"] = F"{self._get_memory_usage()} MB"
        self.metrics["Actors"] = F"{len(Actor.actors)} [{Counter([type(i) for i in Actor.actors]).most_common()[0]}]"
        self.metrics["Room"] = F"{self.get_world().room.coordinates} (Y,X)"
        self.metrics[
            "Position"] = F"{int(self.get_world().get_my_player().pos[0])}, {int(self.get_world().get_my_player().pos[1])}"

    @debug
    def draw(self, screen):
        self._draw_grid(screen)
        self._draw_panel(screen)
        self._draw_collision(screen)

    def _draw_grid(self, screen):
        w, h = screen.get_size()
        line_size = 80
        buffer = 20
        total = line_size + buffer
        for i in range((h // total) + 1):
            pygame.draw.line(screen, (255, 255, 255), (w // 2, i * total), (w // 2, i * total + line_size), 1)

        for i in range((w // total) + 1):
            pygame.draw.line(screen, (255, 255, 255), (i * total, h // 2), (i * total + line_size, h // 2), 1)

    def _draw_collision(self, screen):
        player = self.get_world().get_my_player()
        room = self.get_world().room
        if not player:
            return
        for actor in self.actors:
            if hasattr(actor, "rect"):
                offset_x = player.offset_position[0] + actor.rect.x
                offset_y = player.offset_position[1] + actor.rect.y
                rect = pygame.rect.Rect(offset_x, offset_y, actor.rect.w, actor.rect.h)
                pygame.draw.rect(screen, (255, 0, 100), rect, 1)

    def _draw_panel(self, screen):
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

        self._add_actors_to_panel(panel)
        screen.blit(panel, (screen.get_width() - panel_size[0], 0))

    def _add_actors_to_panel(self, panel):
        # Draw actor list
        top = 8 + (len(self.metrics.items()) + 1) * 2 * self.font.get_height()
        panel_size = panel.get_size()
        bot = panel_size[1] - 8
        sorted_counts = sorted(Counter([(str(type(i))) for i in Actor.actors]).items(), key=lambda x: (-x[1], x[0]))
        for i, (cls, count) in enumerate(sorted_counts):
            text = self.font.render(F'{cls[cls.rfind(".")+1: cls.rfind(">")-1]}: {count}', True, (255, 255, 255))
            panel.blit(text, (8, top + i * 2 * self.font.get_height()))
            next_line = top + (i+1) * 2 * self.font.get_height()
            if next_line > panel_size[1]:
                break


    def _get_client_metrics(self):
        return self.get_world().client.get_incoming_kb_metric()

    def _get_memory_usage(self):
        process = psutil.Process(os.getpid())
        return process.memory_info().rss // (1024 * 1024)

    def _update_fps_counter(self):
        if time() - self.time_since_last_fps_reset > 1:
            self.time_since_last_fps_reset = time()
            self.last_fps = self.fps_incrementer
            self.fps_incrementer = 0
        self.fps_incrementer += 1
