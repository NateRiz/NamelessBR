from Networking.Serializable import Serializable


class DeleteProjectile(Serializable):
    def __init__(self, my_id=None):
        self.my_id = my_id
