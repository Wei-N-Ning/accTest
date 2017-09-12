
import imp
import os

from accTest import exceptions
from accTest.shareable import tasks


def findTaskFile(dslFilePath, taskName, dslExt='.py', taskExt='.py'):
    """
    Searches for ./$DSL/$TASK.py
    """
    taskDir = dslFilePath.replace(dslExt, '')
    taskFilePath = os.path.join(taskDir, '{}{}'.format(taskName, taskExt))
    if os.path.isfile(taskFilePath):
        return taskFilePath
    return ''


def importPythonModule(pythonFilePath):
    """

    Args:
        pythonFilePath (str): ./$DSL/$TASK.py

    Returns:
        module: a module object or None if fail to import
    """
    pythonFileDir = os.path.dirname(pythonFilePath)
    pythonFileName = os.path.basename(pythonFilePath).replace('.py', '')
    try:
        fileHandle, moduleFilePath, description = imp.find_module(pythonFileName, [pythonFileDir])
        mod = imp.load_module(pythonFileName, fileHandle, moduleFilePath, description)
        fileHandle.close()
        return mod
    except (ImportError, Exception), e:
        raise exceptions.CanNotLoadTask(pythonFilePath, pythonFileName, msg=str(e))


class TaskFactory(object):

    TYPE_INSTANCE_SEP = ':'

    def __init__(self, dslFilePath):
        self._dslFilePath = dslFilePath

    def _createFromSharedModule(self, dslTaskName):
        cls = getattr(tasks, dslTaskName, None)
        if not cls:
            return None
        return cls

    def _createFromDslPath(self, dslTaskName):
        taskFilePath = findTaskFile(self._dslFilePath, dslTaskName)
        if not taskFilePath:
            return None
        mod = importPythonModule(taskFilePath)
        cls = getattr(mod, dslTaskName, None)
        if not cls:
            return None
        return cls

    def create(self, dslTaskName):
        taskName, instanceName = self._parseDslTaskName(dslTaskName)
        cls = self._createFromSharedModule(taskName)
        if not cls:
            cls = self._createFromDslPath(taskName)
        if not cls:
            return None
        return self._instantiateClass(cls, instanceName=instanceName)

    def _parseDslTaskName(self, dslTaskName):
        tokens = dslTaskName.split(self.TYPE_INSTANCE_SEP)
        if len(tokens) == 1:
            return dslTaskName, ''
        if len(tokens) == 2:
            return tokens[0], tokens[1]
        raise exceptions.MalformedTaskName(dslTaskName)

    def _instantiateClass(self, cls, instanceName=''):
        return cls(instanceName=instanceName)
