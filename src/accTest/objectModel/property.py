

class Property(object):

    def __init__(self, name, value=None):
        self._name = name
        self._value = value

    def name(self):
        return self._name

    def value(self):
        return self._value
