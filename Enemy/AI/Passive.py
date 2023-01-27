from Enemy.AI.BaseAI import BaseAI


class Passive(BaseAI):
    def __init__(self, enemy):
        super().__init__(enemy)

    def update(self):
        self._wander()
