from Enemy.AI.BaseAI import BaseAI


class Passive(BaseAI):
    def __init__(self, _id, enemy):
        super().__init__(_id, enemy)

    def update(self):
        self._wander()

    def server_update(self):
        if self.should_change_position():
            self._generate_new_wander_position()
        self.update()
