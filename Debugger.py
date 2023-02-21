from time import time
from collections import Counter
import pygame
import os
import psutil

from Engine.Actor import Actor
from Engine.Debug import debug, DebugShape
from Engine.DrawLayer import DrawLayer
from MessageMapper import MessageMapper
from Serializable.Empty import Empty


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
        self.time_since_last_server_message = time()
        self.server_metrics = None

    @debug
    def _update(self):
        """
        Updates metrics every frame
        """
        self._update_fps_counter()
        self._get_server_metrics()

        self.metrics["FPS"] = F"{self.last_fps}"
        self.metrics["Player Id"] = self.get_world().my_id
        self.metrics["Client Incoming"] = F"{self._get_client_metrics()} KB/s"
        self.metrics["Memory"] = F"{self._get_memory_usage()} MB"
        self.metrics["Actors"] = F"{len(Actor.actors)} [{Counter([type(i) for i in Actor.actors]).most_common()[0]}]"
        self.metrics["Room"] = F"{self.get_world().room.coordinates} (Y,X)"
        self.metrics[
            "Position"] = F"{int(self.get_world().get_my_player().pos[0])}, {int(self.get_world().get_my_player().pos[1])}"

        # Server metrics
        if not self.server_metrics:
            return
        self.metrics["Server Actors"] = F"{self.server_metrics.actors}"

    @debug
    def _draw(self, screen):
        self._draw_grid(screen)
        self._draw_panel(screen)
        self._draw_debug_functions(screen)

    def _draw_grid(self, screen):
        w, h = screen.get_size()
        line_size = 80
        buffer = 20
        total = line_size + buffer
        for i in range((h // total) + 1):
            pygame.draw.line(screen, (255, 255, 255), (w // 2, i * total), (w // 2, i * total + line_size), 1)

        for i in range((w // total) + 1):
            pygame.draw.line(screen, (255, 255, 255), (i * total, h // 2), (i * total + line_size, h // 2), 1)

    def _draw_collision(self, screen, actor, player):
        if hasattr(actor, "rect"):
            offset_x = player.offset_position[0] + actor.rect.x
            offset_y = player.offset_position[1] + actor.rect.y
            rect = pygame.rect.Rect(offset_x, offset_y, actor.rect.w, actor.rect.h)
            pygame.draw.rect(screen, (255, 0, 100), rect, 1)

    def _draw_debug_functions(self, screen):
        player = self.get_world().get_my_player()
        if not player:
            return

        for actor in self.actors:
            self._draw_collision(screen, actor, player)
            for name in dir(actor.__class__):
                func = getattr(actor, name)
                if not hasattr(func, "_debug"):
                    continue

                rect = func()
                offset_x = player.offset_position[0] + rect.x
                offset_y = player.offset_position[1] + rect.y
                match func._debug_shape:
                    case DebugShape.RECTANGLE:
                        pygame.draw.rect(screen, func._debug, (offset_x, offset_y, rect.w, rect.h), 1)
                    case DebugShape.CIRCLE:
                        pygame.draw.circle(screen, func._debug, (offset_x, offset_y), rect.w, 1)
                    case _:
                        print(f"Couldn't find debug shape for {func._debug_shape}")



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

    def _get_server_metrics(self):
        if self.get_world().my_id != 0:
            return

        if time() - self.time_since_last_server_message >= 4:
            self.time_since_last_server_message = time()
            self.send_to_server({MessageMapper.SERVER_METRICS_REQUEST: Empty()})

    def set_server_metrics(self, server_metrics):
        self.server_metrics = server_metrics
