import sys

import pygame
from pygame import locals
from Engine.Screen import Screen
from GUI.Button import Button
from Menu.Lobby import Lobby
from Menu.LobbyState import LobbyState


class Menu:
    """
    Startup menu for host and join
    """
    def __init__(self, network, lobby_state):
        self.network = network
        self.lobby_state = lobby_state
        self.screen = Screen().screen
        self.animating_wall_rect: pygame.rect.Rect | None = None
        self.play_button: Button | None = None
        self.join_button: Button | None = None
        self.host_button: Button | None = None
        self.chosen_lobby = LobbyState.TRANSITION_TO_JOIN
        self._set_up_buttons()
        self.buttons = [self.play_button, self.host_button, self.join_button]

    def _set_up_buttons(self):
        center_x = self.screen.get_width() // 2
        center_y = self.screen.get_height() // 2
        size = [256, 96]
        buffer = size[1] // 2
        current_height = center_y - 200
        self.play_button = Button(
            pygame.rect.Rect(center_x - size[0] // 2, current_height - size[1] // 2, size[0], size[1]),
            lambda: print("clicked"), "Play")
        current_height += size[1] + buffer
        self.host_button = Button(
            pygame.rect.Rect(center_x - size[0] // 2, current_height - size[1] // 2, size[0], size[1]),
            self._on_click_host, "Host")
        current_height += size[1] + buffer
        self.join_button = Button(
            pygame.rect.Rect(center_x - size[0] // 2, current_height - size[1] // 2, size[0], size[1]),
            self._on_click_join, "Join")

    def draw(self):
        """
        Draw the buttons on the screen
        """
        self.screen.fill((15, 15, 15))
        for button in self.buttons:
            button.draw(self.screen)

        if self.animating_wall_rect:
            pygame.draw.rect(self.screen, self.play_button.color, self.animating_wall_rect, 2)

    def update(self):
        """
        animate the buttons into the next screen
        """
        if self.animating_wall_rect:
            center_y = self.screen.get_height() // 2
            y = center_y - Lobby.HEIGHT // 2
            x = 32

            move_px = 32
            is_done = True
            if self.animating_wall_rect.x > x:
                self.animating_wall_rect.x = max(self.animating_wall_rect.x - move_px, x)
                is_done = False
            if self.animating_wall_rect.y > y:
                self.animating_wall_rect.y = max(self.animating_wall_rect.y - move_px, y)
                is_done = False
            if self.animating_wall_rect.width < Lobby.WIDTH:
                self.animating_wall_rect.width = min(self.animating_wall_rect.width + 2 * move_px, Lobby.WIDTH)
                is_done = False
            if self.animating_wall_rect.height < Lobby.HEIGHT:
                self.animating_wall_rect.height = min(self.animating_wall_rect.height + 2 * move_px, Lobby.HEIGHT)
                is_done = False
            if is_done:
                self.lobby_state.set(self.chosen_lobby)

    def _on_click_join(self):
        self._hide_and_disable_buttons()
        self._transition_to_online_lobby(self.join_button.rect)
        self.chosen_lobby = LobbyState.TRANSITION_TO_JOIN

    def _on_click_host(self):
        self._hide_and_disable_buttons()
        self.network.create_host()
        self._transition_to_online_lobby(self.host_button.rect)
        self.chosen_lobby = LobbyState.TRANSITION_TO_HOST

    def _transition_to_online_lobby(self, rect):
        self.animating_wall_rect = pygame.rect.Rect(rect)

    def _hide_and_disable_buttons(self):
        for button in self.buttons:
            button.set_disabled()
            button.set_hidden(True)

    def poll_input(self):
        """
        Polls clicks for the buttons
        """
        for event in pygame.event.get():
            if event.type == locals.QUIT:
                pygame.quit()
                sys.exit()
            for button in self.buttons:
                button.poll_input(event)
