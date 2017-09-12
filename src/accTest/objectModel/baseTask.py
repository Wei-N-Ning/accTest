
import weakref

from accTest import exceptions
from accTest.objectModel import registry
from accTest.objectModel import result


class BaseTask(object):

    __metaclass__ = registry.Registry

    def __init__(self, *args, **kwargs):
        self._args = args
        self._fixtureRef = None
        self._instanceName = kwargs.get('instanceName', '')

    def attachToFixture(self, f):
        self._fixtureRef = weakref.ref(f)

    def getFixture(self):
        if self._fixtureRef:
            return self._fixtureRef()
        return None

    def arguments(self):
        return self._args

    def getValue(self, name):
        if not self.getFixture():
            raise exceptions.BrokenTask(self)
        f = self.getFixture()
        return f.getValue(name)

    def createResult(self, state, msg=''):
        f = self.getFixture()
        return result.Result('{}.{}'.format(f.name(), self.fullName()), state, msg=msg)

    def run(self):
        """

        Returns:
            result.Result
        """
        if not self.getFixture():
            raise exceptions.BrokenTask(self)
        result_ = self._run()
        if not isinstance(result_, result.Result):
            result_ = self.fatal('Task {} must return an instance of Result class!'.format(self))
        return result_

    def _run(self):
        """

        Returns:
            result.Result
        """
        return self.createResult(False)

    def name(self):
        return self.__class__.__name__

    def instanceName(self):
        return self._instanceName

    def fullName(self):
        baseName = self.name()
        f = self.getFixture()
        if f:
            baseName = '{}.{}'.format(f.name(), baseName)
        if self._instanceName:
            return ':'.join((baseName, self._instanceName))
        return baseName

    def fatal(self, msg):
        return result.Result(self.fullName(), False, msg=msg)

    def success(self, msg=''):
        return result.Result(self.fullName(), True, msg=msg)
