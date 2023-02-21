class Enemy:
    def __init__(self, my_id, enemy_type, position, target_position, health):
        self.my_id = my_id
        self.enemy_type = enemy_type
        self.position = position
        self.target_position = target_position
        self.health = health
