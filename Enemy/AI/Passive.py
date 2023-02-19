from Enemy.AI.BaseAI import BaseAI


class Passive(BaseAI):
    def __init__(self, _id, enemy):
        super().__init__(_id, enemy)

    def _update(self):
        self._wander()

    def _server_update(self):
        super()._server_update()
        if self._is_marked_for_deletion:
            return

        if self.should_change_position():
            self._generate_new_wander_position()
        self._update()
