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
        object_vars = len(obj)
        self.__dict__.update(obj)
        assert object_vars == len(vars(
            self)), f"Object has gained unexpected class attributes: Found {vars(self)}. Expected only {object_vars}"
        return self

    @staticmethod
    def serialize(obj: object):
        """
        Default function to plug into 'json.dumps' to serialize purely data classes
        :param obj: object to serialize
        :return: dictionary of instance
        """
        return vars(obj)
