class Serializable:
    """
    Base class for serializing and deserializing objects with json sent over the socket
    """
    def load(self, obj: dict):
        """
        Update the instance using the retrieved json dict
        :param obj: dict to update instance
        :return: self
        """
        self.__dict__.update(obj)
        return self

    @staticmethod
    def serialize(obj: object):
        """
        Default function to plug into 'json.dumps' to serialize purely data classes
        :param obj: object to serialize
        :return: dictionary of instance
        """
        return vars(obj)
