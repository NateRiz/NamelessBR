import pygame

from Enemy.Body.BaseEnemy import BaseEnemy
from Enemy.Body.EnemyColor import EnemyColor
from Enemy.Body.EnemyType import EnemyType


class Cleft(BaseEnemy):
    def __init__(self):
        super().__init__()
        self.enemy_type = EnemyType.CLEFT
        self.size = 12
        self.max_speed = 3
        self.max_health = 3
        self.health = self.max_health
        self.collision_size = self.size
        pygame.draw.circle(self.surface, EnemyColor.PASSIVE,
                           (self.surface.get_width() // 2, self.surface.get_height() // 2), self.size)
        pygame.draw.circle(self.surface, EnemyColor.AGGRESSIVE,
                           (self.surface.get_width() // 2, self.surface.get_height() // 2), self.size-4)
