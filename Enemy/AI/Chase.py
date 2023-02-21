from typing import Any

import pygame

from Enemy.AI.BaseAI import BaseAI
from Engine.Debug import debug_draw, DebugShape
from Player import Player
from Serializable.EnemyChase import EnemyChase
from Utility import distance

class Chase(BaseAI):
    def __init__(self, _id, enemy):
        super().__init__(_id, enemy)
        self.sight_distance = 1024
        self.closest_player_id = -1
        self.last_message_sent_chase = EnemyChase(None, None)

    def _update(self):
        self._move_to_current_target()

    @debug_draw((255, 0, 255), DebugShape.CIRCLE)
    def _debug_sight_distance(self):
        return pygame.rect.Rect((*self.enemy.position, self.sight_distance, self.sight_distance))

    def _look_for_player(self):
        players = self.find_objects_by_type(Player)
        if not players:
            return

        closest_player = min(players, key=lambda p: distance(*p.pos, *self.enemy.position))
        if distance(*closest_player.pos, *self.enemy.position) > self.sight_distance:
            self.closest_player_id = -1
        else:
            self.closest_player_id = closest_player.my_id
            self.target_position = closest_player.pos

    def _server_update(self):
        super()._server_update()
        if self._is_marked_for_deletion:
            return

        self._look_for_player()
        if self.closest_player_id == -1 and self.should_change_position():
                self._generate_new_wander_position()
        self._update()

    def get_serialized_deltas(self) -> Any:
        are_any_deltas = False
        base_deltas = super().get_serialized_deltas()

        serialized_deltas = EnemyChase(base_deltas, None)
        # Change in enemy health
        if self.closest_player_id != self.last_message_sent_chase.closest_player_id:
            serialized_deltas.closest_player_id = self.closest_player_id
            self.last_message_sent_chase.closest_player_id = self.closest_player_id
            are_any_deltas = True

        if are_any_deltas or base_deltas:
            return serialized_deltas

    def update_from_serialized(self, enemy_update):
        super().update_from_serialized(enemy_update.enemy)
        if enemy_update.closest_player_id is not None:
            self.closest_player_id = enemy_update.closest_player_id
