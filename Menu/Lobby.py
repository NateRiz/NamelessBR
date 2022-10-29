import sys

import pygame
from pygame import locals

from Engine.Screen import Screen
from Player import Player


class Lobby:
    WIDTH = 1400
    HEIGHT = 1000

    def __init__(self):
        self.is_in_lobby = True
        self.player = Player()

    def update(self):
        self.player.update()

    def draw(self):
        screen = Screen().screen
        screen.fill((15, 15, 15))
        center_y = screen.get_height() // 2
        y = center_y - Lobby.HEIGHT // 2
        x = 32
        self.player.draw()
        pygame.draw.rect(screen, (0, 245, 255), (x, y, Lobby.WIDTH, Lobby.HEIGHT), 2)

    def poll_input(self):
        for event in pygame.event.get():
            if event.type == locals.QUIT:
                pygame.quit()
                sys.exit()
            self.player.poll_input(event)

