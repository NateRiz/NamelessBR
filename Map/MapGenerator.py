from math import floor
from random import randint
import pygame
from pygame.locals import QUIT


class MapGenerator:
    def __init__(self, num_players):
        self.num_players = num_players
        self.map_length = 30
        self.map_width = 30
        self.map = []
        self.end_room = [-1, -1]
        self.players = [[-1, -1] for _ in range(self.num_players)]

    def draw(self):
        # Pygame
        pygame.init()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((1920, 1080))
        while True:
            screen.fill((0, 0, 0))

            buffer = 2
            w_size = floor(screen.get_size()[0] / self.map_width) - buffer
            h_size = floor(screen.get_size()[1] / self.map_length) - buffer
            for i, row in enumerate(self.map):
                for j, col in enumerate(row):
                    color = (165, 165, 165)
                    if col is None:
                        color = (10, 10, 10)
                    pygame.draw.rect(screen, color,
                                     (j * (buffer + w_size), i * (buffer + h_size), w_size, h_size))

            pygame.draw.rect(screen, (100, 255, 100), (
                self.end_room[1] * (buffer + w_size), self.end_room[0] * (buffer + h_size), w_size, h_size))

            for player in self.players:
                pygame.draw.rect(screen, (100, 100, 255), (
                    player[1] * (buffer + w_size), player[0] * (buffer + h_size), w_size, h_size))

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()

            clock.tick()
            pygame.display.flip()

    def generate(self):
        self._create_base_map()

    def _create_base_map(self):
        self.map = [[None for i in range(self.map_length)] for _ in range(self.map_width)]
        self._place_players_and_end_room()

    def _place_players_and_end_room(self):
        min_spacing_distance = 15
        are_entities_placed = False
        player_coord_generator = self._get_random_coordinate_on_next_side()
        while not are_entities_placed:
            are_entities_placed = True
            self.end_room = [randint(1, len(self.map) - 2), randint(1, len(self.map[0]) - 2)]
            self.players = [next(player_coord_generator) for _ in range(len(self.players))]
            entities = self.players + [self.end_room]
            for i, src in enumerate(entities[:-1]):
                if not are_entities_placed:
                    break
                for dst in entities[i + 1:]:
                    distance = abs(src[0] - dst[0]) + abs(src[1] - dst[1])
                    if distance < min_spacing_distance:
                        are_entities_placed = False
                        break

    def _get_random_coordinate_on_next_side(self):
        while 1:
            yield [0, randint(2, len(self.map) - 2)]
            yield [len(self.map[0]) - 1, randint(2, len(self.map) - 2)]
            yield [randint(2, len(self.map[0]) - 2), 0]
            yield [randint(2, len(self.map[0]) - 2), len(self.map) - 1]
