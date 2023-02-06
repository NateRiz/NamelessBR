from math import floor
import pygame
from pygame.locals import QUIT
from random import seed, randint, shuffle


class MapGenerator:
    def __init__(self, player_ids, map_size):
        self.map_length = map_size
        self.map_width = map_size
        self.map = []
        self.end_room = [-1, -1]
        self.players = {i: [-1, -1] for i in player_ids}

    def debug_draw_map(self):
        pygame.init()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((1920, 1080))
        while True:
            screen.fill((0, 0, 0))
            buffer = 2
            w_size = floor(screen.get_size()[0] / self.map_width) - buffer
            h_size = floor(screen.get_size()[1] / self.map_length) - buffer
            for i, row in enumerate(self.map):
                for j, room in enumerate(row):
                    seed(10 + room.difficulty)
                    color = [randint(120, 200), randint(120, 200), randint(120, 200)]
                    # shuffle(color)
                    pygame.draw.rect(screen, color,
                                     (j * (buffer + w_size), i * (buffer + h_size), w_size, h_size))

            pygame.draw.rect(screen, (0, 255, 0), (
                self.end_room[1] * (buffer + w_size), self.end_room[0] * (buffer + h_size), w_size, h_size))

            for player in self.players:
                pygame.draw.rect(screen, (0, 0, 255), (
                    player[1] * (buffer + w_size), player[0] * (buffer + h_size), w_size, h_size))

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return

            clock.tick()
            pygame.display.flip()

    def generate(self):
        self._create_base_map()
        return self.map

    def _create_base_map(self):
        #self.map = [[RoomFactory.create([y, x], self.map_width) for x in range(self.map_length)] for y in range(self.map_width)]
        self.map = [[None for x in range(self.map_length)] for y in range(self.map_width)]
        self._place_players_and_end_room()

    def _place_players_and_end_room(self):
        min_spacing_distance = 15
        are_entities_placed = False
        player_coord_generator = self._get_random_coordinate_on_next_side()
        while not are_entities_placed:
            are_entities_placed = True
            end_room_distance_from_walls = 10
            self.end_room = [randint(end_room_distance_from_walls, len(self.map) - end_room_distance_from_walls),
                             randint(end_room_distance_from_walls, len(self.map[0]) - end_room_distance_from_walls)]
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
        """
        min_difficulty = min_spacing_distance
        for i, r in enumerate(self.map):
            for j, rm in enumerate(r):
                distance_from_end = abs(i - self.end_room[0]) + abs(j - self.end_room[1])
                rm.difficulty = min(min_difficulty, distance_from_end)
        """

    def _get_random_coordinate_on_next_side(self):
        while 1:
            yield [0, randint(2, len(self.map) - 2)]
            yield [len(self.map[0]) - 1, randint(2, len(self.map) - 2)]
            yield [randint(2, len(self.map[0]) - 2), 0]
            yield [randint(2, len(self.map[0]) - 2), len(self.map) - 1]
