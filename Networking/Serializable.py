class Serializable:
    def load(self, obj):
        self.__dict__.update(obj)
        return self

    @staticmethod
    def serialize(obj: object):
        return vars(obj)
