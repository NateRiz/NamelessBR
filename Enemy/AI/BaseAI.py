from math import sqrt, copysign
from time import time

from Enemy.AI.AIState import AIState
from Enemy.Body.BaseEnemy import BaseEnemy
from Engine.Actor import Actor

from random import randint
import Serializable.Enemy
from Settings import Settings


class BaseAI(Actor):
    id_incrementer = -1

    def __init__(self, _id: int, enemy: BaseEnemy):
        super().__init__()
        self.my_id = _id
        if _id == -1:  # Created by server
            BaseAI.id_incrementer += 1
            self.my_id = BaseAI.id_incrementer
        self.add_child(enemy)
        self.enemy = enemy
        self.ai_state = AIState.NONE
        self.target_position: list[int] = list(self.enemy.position)
        self.last_message_sent = Serializable.Enemy.Enemy()
        self.time_since_last_position_sent = time()

    def _wander(self):
        enemy_x, enemy_y = self.enemy.position
        dst_x, dst_y = self.target_position
        vector = [dst_x - enemy_x, dst_y - enemy_y]
        normalized = [copysign(1, vector[0]), copysign(1, vector[1])]
        if abs(vector[0]) < self.enemy.size:
            normalized[0] = 0
        if abs(vector[1]) < self.enemy.size:
            normalized[1] = 0
        self.enemy.move(normalized)

    def _generate_new_wander_position(self):
        buffer = 4
        room_w = Settings.ROOM_WIDTH
        room_h = Settings.ROOM_WIDTH
        self.target_position = [randint(buffer, room_w - buffer), randint(buffer, room_h - buffer)]

    def should_change_position(self):
        if self.target_position is None:
            return True
        enemy_x, enemy_y = self.enemy.position
        dst_x, dst_y = self.target_position
        if abs(dst_x - enemy_x) <= self.enemy.size and abs(dst_y - enemy_y) <= self.enemy.size:
            return True
        return False

    def get_serialized_deltas(self) -> Serializable.Enemy.Enemy | None:
        """ Creates an object to be sent that contains only necessary differences from the last update. """
        serialized_deltas = Serializable.Enemy.Enemy(self.my_id, None, None, None)
        are_any_deltas = False
        if self.last_message_sent.target_position != self.target_position:
            serialized_deltas.target_position = list(self.target_position)
            self.last_message_sent.target_position = list(self.target_position)
            are_any_deltas = True

        if time() - self.time_since_last_position_sent > 2:  # 2 sec
            serialized_deltas.position = [int(self.enemy.position[0]), int(self.enemy.position[1])]
            self.last_message_sent.position = list(serialized_deltas.position)
            self.time_since_last_position_sent = time()
            are_any_deltas = True

        if self.enemy.health != self.last_message_sent.health:
            serialized_deltas.health = self.enemy.health
            self.last_message_sent.health = self.enemy.health
            are_any_deltas = True

        if not are_any_deltas:
            return None

        return serialized_deltas

    def get_serialized(self):
        """ Creates an object to be sent that contains all information for this enemy """
        return Serializable.Enemy.Enemy(self.my_id, self.enemy.enemy_type, self.enemy.position)
