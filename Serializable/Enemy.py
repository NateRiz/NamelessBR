class Enemy:
    def __init__(self, my_id=None, enemy_type=None, position=None, target_position=None, health=None):
        self.my_id = my_id
        self.enemy_type = enemy_type
        self.position = position
        self.target_position = target_position
        self.health = health
