import pygame

from Networking.Network import Network
from Menu.Menu import Menu
from Engine.Game import Game
from Engine import Actor
from Menu.Lobby import Lobby
from Menu.LobbyState import LobbyState
from Menu.LobbyStateContainer import LobbyStateContainer
from World import World


class GameState:
    def __init__(self):
        pygame.init()
        Actor.ActorManager.static_init_actor()
        self.clock = pygame.time.Clock()
        self.network = Network()
        self.lobby_state = LobbyStateContainer()
        self.lobby_state.set(LobbyState.TRANSITION_TO_MENU)
        self.menu = Menu(self.network, self.lobby_state)
        self.lobby = Lobby(self.network, self.lobby_state)
        self.game = None

    def start(self):
        while 1:
            match self.lobby_state.lobby_state:
                case LobbyState.TRANSITION_TO_JOIN:
                    self.join_loop()
                case LobbyState.TRANSITION_TO_HOST:
                    self.host_loop()
                case LobbyState.TRANSITION_TO_MENU:
                    self.menu_loop()
                case LobbyState.TRANSITION_TO_GAME:
                    self.game = Game(self.network)
                    self.game.main_loop(World())



    def menu_loop(self):
        self.lobby_state.set(LobbyState.MENU)
        while self.lobby_state.lobby_state == LobbyState.MENU:
            self.clock.tick(60)
            self.menu.poll_input()
            self.menu.update()
            self.menu.draw()
            pygame.display.flip()

    def host_loop(self):
        self.lobby_state.set(LobbyState.HOST)
        while self.lobby_state.lobby_state == LobbyState.HOST:
            self.clock.tick(60)
            self.lobby.poll_input()
            self.lobby.update()
            self.lobby.draw()
            pygame.display.flip()

    def join_loop(self):
        self.lobby_state.set(LobbyState.JOIN)
        while self.lobby_state.lobby_state == LobbyState.JOIN:
            self.clock.tick(60)
            self.lobby.poll_input()
            self.lobby.update()
            self.lobby.draw()
            pygame.display.flip()
