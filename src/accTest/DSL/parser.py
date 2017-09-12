
import os

from accTest import exceptions
from accTest.DSL import factory
from accTest.objectModel import fixture


class TaskProxy(object):
    """
    To defer instantiate the task
    """

    def __init__(self, dslFilePath, dslTaskName):
        self._dslFilePath = dslFilePath
        self._dslTaskName = dslTaskName
        self._taskFactory = factory.TaskFactory(dslFilePath)

    def fullName(self):
        return self._dslTaskName

    def instantiate(self):
        task = self._taskFactory.create(self._dslTaskName)
        if task is None:
            raise exceptions.CanNotLoadTask(self._dslFilePath, self._dslTaskName, msg='fail to instantiate')
        return task


class Parser(object):

    def __init__(self):
        self._taskFactory = None
        self._dslFilePath = ''

    def parse(self, dslFilePath, indexes=None):
        if not (dslFilePath and os.path.isfile(dslFilePath)):
            raise exceptions.InvalidDslFilePath(dslFilePath)
        self._dslFilePath = dslFilePath
        mod = factory.importPythonModule(dslFilePath)
        fixtures = []
        globalSettings = self._getModuleGlobalSettings(mod)
        for idx, cls in enumerate(self._iterModuleClasses(mod)):
            if indexes and idx not in indexes:
                continue
            f = self._generateFixtureFromDslClass(cls, globalSettings=globalSettings)
            fixtures.append(f)
        self._dslFilePath = ''
        return fixtures

    def _iterModuleClasses(self, mod):
        for symbol in dir(mod):
            if symbol.startswith('_'):
                continue
            obj = getattr(mod, symbol)
            if isinstance(obj, type):
                yield obj

    def _getModuleGlobalSettings(self, mod):
        globalSettings = dict()
        for symbol in dir(mod):
            if symbol.startswith('_'):
                continue
            obj = getattr(mod, symbol)
            if not isinstance(obj, type):
                globalSettings[symbol] = obj
        return globalSettings

    def _generateFixtureFromDslClass(self, cls, globalSettings=None):
        f = fixture.Fixture(name=cls.__name__)
        if globalSettings and isinstance(globalSettings, dict):
            for globalK, globalV in globalSettings.iteritems():
                f.setValue(globalK, value=globalV)
        for name in dir(cls):
            if name.startswith('_'):
                continue
            value = getattr(cls, name)
            if name == 'tasks':
                for dslTaskName in value:
                    f.addTaskProxy(TaskProxy(self._dslFilePath, dslTaskName))
            else:
                f.setValue(name, value=value)
        return f
