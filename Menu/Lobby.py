import sys
import pygame
from pygame import locals
from Engine.Screen import Screen
from GUI.Button import Button
from GUI.InputBox import InputBox
from Menu.LobbyState import LobbyState
from Menu.PlayerContainer import PlayerContainer
from Networking.Network import Network


class Lobby:
    WIDTH = 1400
    HEIGHT = 1000

    def __init__(self, network, lobby_state_container):
        self.network: Network = network
        self.lobby_state = lobby_state_container
        self.ip_input = InputBox(pygame.rect.Rect(0, 0, 0, 0)).connect(self.connect_to_host)
        self.ip_input.value = "127.0.0.1"
        self.start_button = Button(pygame.rect.Rect(0, 0, 0, 0), self._start_game, "Start")
        self.start_button.set_disabled()
        self.start_button.set_hidden(True)
        self.lobby_rect = pygame.rect.Rect(0, 0, 0, 0)
        screen_availability = self._setup_screen()
        self.player_container = PlayerContainer(self.network, screen_availability)

    def update(self):
        if self.is_host():
            message = self.network.server.get_next_message()
            if message is not None:
                if "on_connect" in message.message:
                    self.player_container.add_player(message.owner_id)
            if self.network.server.get_connected() > 1:
                self.start_button.set_hidden(False)
                self.start_button.set_enabled()

    def draw(self):
        screen = Screen().screen
        screen.fill((15, 15, 15))

        pygame.draw.rect(screen, (0, 245, 255), self.lobby_rect, 2, 8)

        if self.is_host():
            self.start_button.draw(screen)

        if self.is_connected():
            self.player_container.draw(screen)
        else:
            self.ip_input.draw(screen)

    def poll_input(self):
        for event in pygame.event.get():
            if event.type == locals.QUIT:
                pygame.quit()
                sys.exit()

            if self.start_button.is_enabled:
                self.start_button.poll_input(event)

            if not self.is_connected():
                self.ip_input.poll_input(event)

    def connect_to_host(self):
        self.network.create_client(self.ip_input.value, 7777)

    def is_connected(self):
        return self.network.client is not None

    def is_host(self):
        return self.network.server is not None

    def _setup_screen(self):
        screen = Screen().screen
        center_y = screen.get_height() // 2
        y = center_y - Lobby.HEIGHT // 2
        lobby_x = 32
        self.lobby_rect = pygame.rect.Rect(lobby_x, y, Lobby.WIDTH, Lobby.HEIGHT)

        ip_w = 300
        ip_h = 100
        ip_x = (screen.get_width() - lobby_x - Lobby.WIDTH) // 2 + (Lobby.WIDTH + lobby_x) - ip_w // 2
        self.ip_input.rect = pygame.rect.Rect(ip_x, y, ip_w, ip_h)

        w = 200
        h = 50
        x = (screen.get_width() - lobby_x - Lobby.WIDTH) // 2 + (Lobby.WIDTH + lobby_x) - w // 2
        start_y = Lobby.HEIGHT + y - h
        self.start_button.rect = pygame.rect.Rect(x, start_y, w, h)

        # return the available screen space to be used by the player containers after connection
        return ip_x, y, ip_w, start_y

    def _start_game(self):
        self.lobby_state.lobby_state = LobbyState.TRANSITION_TO_GAME
