import sys
import pygame
from pygame import locals

from MessageMapper import MessageMapper
from Engine.Screen import Screen
from GUI.Button import Button
from GUI.InputBox import InputBox
from Menu.LobbyState import LobbyState
from Menu.PlayerContainer import PlayerContainer

from Networking.Client import Client
from Serializable.Empty import Empty
from Serializable.ListClientsResponse import ListClientsResponse


class Lobby:
    """
    Multiplayer lobby to see connected clients
    """
    WIDTH = 1400
    HEIGHT = 1000

    def __init__(self, client, lobby_state_container, is_host):
        self.client: Client = client
        self.lobby_state = lobby_state_container
        self.is_host = is_host
        self.ip_input = InputBox(pygame.rect.Rect(0, 0, 0, 0)).connect(self._connect_to_host)
        self.ip_input.value = "127.0.0.1"
        self.start_button = Button(pygame.rect.Rect(0, 0, 0, 0), self._start_game, "Start")
        self.start_button.set_disabled()
        self.start_button.set_hidden(True)
        self.lobby_rect = pygame.rect.Rect(0, 0, 0, 0)
        screen_availability = self._setup_screen()
        self.player_container = PlayerContainer(screen_availability)

    def update(self):
        """
        Wait and handle server messages for adding clients and starting the game
        """
        if self.is_host:
            if len(self.player_container.containers) >= 1:
                self.start_button.set_hidden(False)
                self.start_button.set_enabled()

        if self._is_connected():
            message = self.client.get_next_message()
            if message:
                if MessageMapper.START in message.message:
                    self.lobby_state.lobby_state = LobbyState.TRANSITION_TO_GAME
                if MessageMapper.LIST_CLIENTS_RESPONSE in message.message:
                    response = message.message[MessageMapper.LIST_CLIENTS_RESPONSE]
                    player_ids = response.clients
                    self.player_container.update_players(player_ids)

    def draw(self):
        """
        Draw the lobby
        """
        screen = Screen().screen
        screen.fill((15, 15, 15))

        pygame.draw.rect(screen, (0, 245, 255), self.lobby_rect, 2, 8)

        if self.is_host:
            self.start_button.draw(screen)

        if self._is_connected():
            self.player_container.draw(screen)
        else:
            self.ip_input._draw(screen)

    def poll_input(self):
        """
        polls input from the user
        """
        for event in pygame.event.get():
            if event.type == locals.QUIT:
                pygame.quit()
                sys.exit()

            if self.start_button.is_enabled:
                self.start_button.poll_input(event)

            if not self._is_connected():
                self.ip_input._poll_input(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self.start_button.is_enabled:
                    if self.is_host:
                        self._start_game()

    def _connect_to_host(self):
        self.connect_to_host(self.ip_input.value, 7777)

    def connect_to_host(self, ip: str, port: int):
        """
        Connects the client to the specified host
        """
        self.client.connect(ip, port)
        self.client.send({MessageMapper.LIST_CLIENTS_REQUEST: Empty()})

    def _is_connected(self):
        return self.client.is_connected()

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
        self.client.send({MessageMapper.START: Empty()})
