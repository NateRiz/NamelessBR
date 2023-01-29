import pygame

from Enemy.AI.Passive import Passive
from Enemy.Body.Snail import Snail
from Engine.Actor import Actor
from Engine.DrawLayer import DrawLayer
from Map.Door import Door
from Map.Ground import Ground
from Map.Wall import Wall
from Player import Player


class Room(Actor):
    """
    Contains a player and other entities
    """

    def __init__(self, coordinates):
        super().__init__()
        self.set_draw_layer(DrawLayer.ROOM)
        self.coordinates = coordinates
        self.width = 2500
        self.height = 1500
        self.surface = pygame.Surface((self.width, self.height))
        self.ground = Ground(self.surface)
        self.doors = {}
        self.players = {}
        self.walls = []
        self.snail = Passive(Snail())


    def draw(self, screen):
        """
        Draw the room in relation to the players offset position.
        Current player should always be in the center.
        Everything in the room is drawn to this surface which is also offset
        :param screen: Screen to draw the surface to
        """
        player = self.get_world().get_my_player()
        if not player:
            return
        screen.blit(self.surface, player.offset_position)

    def draw_to_room(self, surface, position):
        """
        Draw an entity to the surface which will be offset by the players position
        :param surface: Offset surface
        :param position: Position relative to the room to draw at
        """
        self.surface.blit(surface, position)

    def get_surface(self):
        """
        Get the offset surface to draw directly to
        :return: Offset surface
        """
        return self.surface

    def add_doors(self):
        """
        Add doors so long as they lead to another room in the map.
        """
        map_size = len(self.get_world().map)
        if self.coordinates[0] > 0:
            self.doors[Door.NORTH] = Door(self.surface, Door.NORTH, (self.coordinates[0] - 1, self.coordinates[1]))

        if self.coordinates[1] + 1 < map_size:
            self.doors[Door.EAST] = Door(self.surface, Door.EAST, (self.coordinates[0], self.coordinates[1] + 1))

        if self.coordinates[0] + 1 < map_size:
            self.doors[Door.SOUTH] = Door(self.surface, Door.SOUTH, (self.coordinates[0] + 1, self.coordinates[1]))

        if self.coordinates[1] > 0:
            self.doors[Door.WEST] = Door(self.surface, Door.WEST, (self.coordinates[0], self.coordinates[1] - 1))

    def add_walls(self):
        wall_size = 64
        top = Wall(pygame.rect.Rect(0, -wall_size, self.width + wall_size, wall_size))
        right = Wall(pygame.rect.Rect(self.width, 0, wall_size, self.height + wall_size))
        left = Wall(pygame.rect.Rect(-wall_size, self.height, self.width + wall_size, wall_size))
        bottom = Wall(pygame.rect.Rect(-wall_size, -wall_size, wall_size, self.height + wall_size))

        self.walls += [top, right, left, bottom]

    def try_add_player(self, player_id, player):
        if player_id in self.players:
            return
        is_me = self.get_world().my_id == player_id
        self.players[player_id] = Player(player_id, is_me)
        self.players[player_id].pos = player.position

    def try_remove_player(self, player_id):
        if player_id not in self.players:
            return
        del self.players[player_id]
