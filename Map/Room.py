import pygame

from Enemy.AI.BaseAI import BaseAI
from Enemy.AI.EnemyFactory import EnemyFactory
from Engine.Actor import Actor
from Engine.DrawLayer import DrawLayer
from Map.Door import Door
from Map.Ground import Ground
from Map.Wall import Wall
from Player import Player
from Projectile.Projectile import Projectile
from Settings import Settings


class Room(Actor):
    """Contains a player and other entities"""
    def __init__(self, coordinates):
        super().__init__()
        self.set_draw_layer(DrawLayer.ROOM)
        self.coordinates = coordinates
        self.surface = pygame.Surface((Settings.ROOM_WIDTH, Settings.ROOM_HEIGHT))
        self.ground = self.add_child(Ground.new(self.surface))
        self.doors: dict[int, Door] = {}
        self.players: dict[int, Player] = {}
        self.walls: list[Wall] = []
        self.projectiles: set[Projectile] = set()
        self.enemies: list[BaseAI] = []

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
        if self.coordinates[0] > 0:
            self.doors[Door.NORTH] = Door.new(self.surface, Door.NORTH, (self.coordinates[0] - 1, self.coordinates[1]))

        if self.coordinates[1] + 1 < Settings.MAP_SIZE:
            self.doors[Door.EAST] = Door.new(self.surface, Door.EAST, (self.coordinates[0], self.coordinates[1] + 1))

        if self.coordinates[0] + 1 < Settings.MAP_SIZE:
            self.doors[Door.SOUTH] = Door.new(self.surface, Door.SOUTH, (self.coordinates[0] + 1, self.coordinates[1]))

        if self.coordinates[1] > 0:
            self.doors[Door.WEST] = Door.new(self.surface, Door.WEST, (self.coordinates[0], self.coordinates[1] - 1))

        for door in self.doors.values():
            self.add_child(door)

    def add_walls(self):
        wall_size = 64
        top = Wall.new(pygame.rect.Rect(0, -wall_size, Settings.ROOM_WIDTH + wall_size, wall_size))
        right = Wall.new(pygame.rect.Rect(Settings.ROOM_WIDTH, 0, wall_size, Settings.ROOM_HEIGHT + wall_size))
        left = Wall.new(pygame.rect.Rect(-wall_size, Settings.ROOM_HEIGHT, Settings.ROOM_WIDTH + wall_size, wall_size))
        bottom = Wall.new(pygame.rect.Rect(-wall_size, -wall_size, wall_size, Settings.ROOM_HEIGHT + wall_size))

        self.walls += [top, right, left, bottom]
        for wall in self.walls:
            self.add_child(wall)

    def try_add_player(self, player_id, player):
        if player_id in self.players:
            return
        is_me = self.get_world().my_id == player_id
        self.players[player_id] = self.add_child(Player.new(player_id, is_me))
        self.players[player_id].pos = player.position

    def try_remove_player(self, player_id):
        if player_id not in self.players:
            return
        self.players[player_id].free()
        del self.players[player_id]

    def spawn_projectile(self, projectile: Projectile):
        self.projectiles.add(projectile)
        self.add_child(projectile)

    def spawn_enemy(self, enemy_type, x, y):
        enemy = EnemyFactory.create(enemy_type)
        enemy.enemy.position = [x, y]
        self.add_child(enemy)
        self.enemies.append(enemy)
