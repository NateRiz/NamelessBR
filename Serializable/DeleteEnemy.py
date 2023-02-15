from Networking.Serializable import Serializable


class DeleteEnemy(Serializable):
    def __init__(self, my_id=None):
        self.my_id = my_id
