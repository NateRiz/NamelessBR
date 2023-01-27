from math import sqrt, copysign

from Enemy.AI.AIState import AIState
from Enemy.Body.BaseEnemy import BaseEnemy
from Engine.Actor import Actor

from random import randint


class BaseAI(Actor):
    def __init__(self, enemy: BaseEnemy):
        super().__init__()
        self.enemy = enemy
        self.ai_state = AIState.NONE
        self.wander_position: list[int] | None = None

    def _wander(self):
        if self.wander_position is None:
            self._generate_new_wander_position()
        enemy_x, enemy_y = self.enemy.position
        dst_x, dst_y = self.wander_position
        if abs(dst_x - enemy_x) <= self.enemy.size and abs(dst_y - enemy_y) <= self.enemy.size:
            self._generate_new_wander_position()
        dst_x, dst_y = self.wander_position
        vector = [dst_x - enemy_x, dst_y - enemy_y]
        normalized = [copysign(1, vector[0]), copysign(1, vector[1])]
        if abs(vector[0]) < self.enemy.size:
            normalized[0] = 0
        if abs(vector[1]) < self.enemy.size:
            normalized[1] = 0
        self.enemy.move(normalized)

    def _generate_new_wander_position(self):
        buffer = 4
        room_w = self.get_world().room.width
        room_h = self.get_world().room.height
        self.wander_position = [randint(buffer, room_w - buffer), randint(buffer, room_h - buffer)]
        print(self.wander_position)
