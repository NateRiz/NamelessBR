class EnemyChase:
    def __init__(self, enemy, closest_player_id):
        self.enemy=enemy
        self.closest_player_id = closest_player_id
        self.my_id = -1
        if enemy is not None:
            self.my_id = self.enemy.my_id
