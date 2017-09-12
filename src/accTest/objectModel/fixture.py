
import collections

from accTest.objectModel import property


class Fixture(object):

    def __init__(self, name=''):
        self._name = name
        self._properties = collections.OrderedDict()
        self._tasks = collections.OrderedDict()
        self._toTerminate = False

    def name(self):
        return self._name

    def hasProperty(self, name):
        return name in self._properties

    def setValue(self, name, value):
        self._properties[name] = property.Property(name, value=value)

    def getValue(self, name):
        p = self._properties.get(name)
        if not p:
            return None
        return p.value()

    def getTasks(self):
        return self._tasks

    def addTask(self, task):
        self._tasks[task.fullName()] = task
        task.attachToFixture(self)

    def addTaskProxy(self, taskProxy):
        self._tasks[taskProxy.fullName()] = taskProxy

    def iterTasks(self):
        for taskName, task in self._tasks.iteritems():
            if self._toTerminate:
                break
            yield task

    def terminate(self):
        self._toTerminate = True
