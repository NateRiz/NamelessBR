import pygame

from Networking.Network import Network
from Menu.Menu import Menu
from Engine.Game import Game
from Menu.Lobby import Lobby
from Menu.LobbyState import LobbyState
from Menu.LobbyStateContainer import LobbyStateContainer
from World import World


class GameState:
    """
    Controls the current screen that we're in
    Menu, Lobby, in-game, etc
    """
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.network = Network()
        self.lobby_state = LobbyStateContainer()
        self.lobby_state.set(LobbyState.TRANSITION_TO_MENU)
        self.menu = Menu(self.network, self.lobby_state)
        self.lobby = Lobby(self.network, self.lobby_state)
        self.game = None

    def start(self):
        """
        Starts GameState main loop
        """
        while 1:
            match self.lobby_state.lobby_state:
                case LobbyState.TRANSITION_TO_JOIN:
                    self._join_loop()
                case LobbyState.TRANSITION_TO_HOST:
                    self._host_loop()
                case LobbyState.TRANSITION_TO_MENU:
                    self._menu_loop()
                case LobbyState.TRANSITION_TO_GAME:
                    self.game = Game(self.network)
                    self.game.main_loop(World(self.network))

    def _menu_loop(self):
        self.lobby_state.set(LobbyState.MENU)
        while self.lobby_state.lobby_state == LobbyState.MENU:
            self.clock.tick(60)
            self.menu.poll_input()
            self.menu.update()
            self.menu.draw()
            pygame.display.flip()

    def _host_loop(self):
        self.lobby.connect_to_host()
        self.lobby_state.set(LobbyState.HOST)
        while self.lobby_state.lobby_state == LobbyState.HOST:
            self.clock.tick(60)
            self.lobby.poll_input()
            self.lobby.update()
            self.lobby.draw()
            pygame.display.flip()

    def _join_loop(self):
        self.lobby_state.set(LobbyState.JOIN)
        while self.lobby_state.lobby_state == LobbyState.JOIN:
            self.clock.tick(60)
            self.lobby.poll_input()
            self.lobby.update()
            self.lobby.draw()
            pygame.display.flip()
