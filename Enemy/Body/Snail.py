import pygame

from Enemy.Body.BaseEnemy import BaseEnemy
from Enemy.Body.EnemyType import EnemyType


class Snail(BaseEnemy):
    def __init__(self):
        super().__init__()
        self.enemy_type = EnemyType.SNAIL
        pygame.draw.circle(self.surface, (0, 128, 255),
                           (self.surface.get_width() // 2, self.surface.get_height() // 2), self.size)
