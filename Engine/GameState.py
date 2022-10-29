import pygame

import Menu.Menu as Menu
from Engine import Actor
from Menu.Lobby import Lobby
from Menu.LobbyState import LobbyState


class GameState:
    def __init__(self):
        pygame.init()
        Actor.ActorManager.static_init_actor()
        self.clock = pygame.time.Clock()

    def start(self):
        menu = Menu.Menu()
        lobby = Lobby()
        while menu.lobby_state == LobbyState.MENU:
            self.clock.tick(60)
            menu.poll_input()
            menu.update()
            menu.draw()
            pygame.display.flip()
        while menu.lobby_state == LobbyState.HOST:
            self.clock.tick(60)
            lobby.poll_input()
            lobby.update()
            lobby.draw()
            pygame.display.flip()
