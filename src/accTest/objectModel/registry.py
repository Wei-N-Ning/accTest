
class Registry(type):

    _registry = dict()

    def __new__(mcs, clsName, *args):
        clsObj = type.__new__(mcs, clsName, *args)
        if clsObj not in mcs._registry:
            mcs._registry[clsName] = clsObj
        return clsObj

    @classmethod
    def getClass(cls, clsName):
        return cls._registry.get(clsName, None)

    @classmethod
    def clear(cls):
        cls._registry.clear()


def get(clsName):
    return Registry.getClass(clsName)


def clear():
    Registry.clear()
