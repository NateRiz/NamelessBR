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
import Serializable.Enemy
from Projectile.Simple import Simple
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
        self.projectiles: dict[int: Projectile] = {}
        self.enemies: dict[int, BaseAI] = {}

    def _draw(self, screen):
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

    def spawn_projectile(self, position, direction):
        projectile = Simple.new(position, direction)
        self.projectiles[projectile.my_id] = projectile
        self.add_child(projectile)
        return projectile

    def remove_projectile(self, my_id: int):
        if my_id in self.projectiles:
            self.projectiles[my_id].free()

    def remove_enemy(self, my_id: int):
        if my_id in self.enemies:
            self.enemies[my_id].free()

    def spawn_enemy(self, _id, enemy_type, x, y):
        enemy = EnemyFactory.create(_id, enemy_type)
        enemy.enemy.position = [x, y]
        self.add_child(enemy)
        self.enemies[enemy.my_id] = enemy

    def update_enemy(self, enemy_update: Serializable.Enemy.Enemy):
        if enemy_update.my_id not in self.enemies:
            return
        enemy = self.enemies[enemy_update.my_id]
        if enemy_update.position is not None:
            enemy.enemy.position = list(enemy_update.position)
        if enemy_update.target_position is not None:
            enemy.target_position = list(enemy_update.target_position)
        if enemy_update.health is not None:
            enemy.enemy.health = enemy_update.health
        return
