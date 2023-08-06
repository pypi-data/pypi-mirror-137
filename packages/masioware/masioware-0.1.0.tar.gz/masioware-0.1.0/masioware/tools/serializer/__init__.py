class Serializer():

    def to_json(self):
        return dict(self.__iter__())

    def __iter__(self):
        for attr in dir(self):
            value = getattr(self, attr)
            if not attr.startswith("__") and not callable(value):
                yield attr, value
