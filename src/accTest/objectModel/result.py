
import sys

import json

from accTest import terminal


class Result(object):

    def __init__(self, name, hasPassed, msg=''):
        self._name = name
        self._hasPassed = hasPassed
        self._msg = msg

    def name(self):
        return self._name

    def hasPassed(self):
        return self._hasPassed

    def msg(self):
        return self._msg

    def __nonzero__(self):
        return self._hasPassed

    def __str__(self):
        return '{}:{}{}'.format(self._name, self._hasPassed, ' - {}'.format(self.msg()) if self.msg() else '')

    def toDict(self):
        return {'name': self.name(), 'hasPassed': self.hasPassed(), 'msg': self.msg()}

    @classmethod
    def fromDict(cls, aDict):
        ins = cls(aDict.get('name', ''), aDict.get('hasPassed', False), msg=aDict.get('msg', ''))
        return ins


class Serializer(object):
    """
    Serialize/Deserialize the result object
    """

    def read(self, filePath):
        with open(filePath, 'r') as fp:
            records = json.load(fp)
        if isinstance(records, (tuple, list)):
            return [Result.fromDict(r) for r in records]
        return [Result.fromDict(records)]

    def write(self, resultOrList, filePath):
        if isinstance(resultOrList, (tuple, list)):
            records = [r.toDict() for r in resultOrList]
        else:
            records = [resultOrList.toDict()]
        with open(filePath, 'w') as fp:
            json.dump(records, fp)


class Printer(object):

    def __init__(self, oStream=None, includeDetails=False):
        self._includeDetails = includeDetails
        if oStream:
            self._oStream = oStream
            self._useShell = False
        else:
            self._oStream = sys.stdout
            self._useShell = True

    def _write(self, text, color=''):
        if self._useShell:
            terminal.printC(text, color=color)
        else:
            self._oStream.write(text)
            self._oStream.write('\n')

    def _printHeader(self):
        self._write('=' * 16)

    def _printTitle(self, result):
        self._write('- {}'.format(result.name()), color='green' if result.hasPassed() else 'red')

    def _printState(self, result):
        self._write('Passed' if result.hasPassed() else 'Failed', color='green' if result.hasPassed() else 'red')

    def _printDetails(self, result):
        self._write('Details:\n{}'.format(result.msg()))

    def _printTail(self):
        self._write('-' * 16)

    def prt(self, result):
        self._printHeader()
        self._printTitle(result)
        self._printState(result)
        if self._includeDetails:
            self._printDetails(result)
        self._printTail()


def write(results, filePath):
    return Serializer().write(results, filePath)


def read(filePath):
    try:
        return Serializer().read(filePath)
    except (ValueError, Exception), e:
        return None


def prt(results, includeDetails=False):
    p = Printer(includeDetails=includeDetails)
    for r in results:
        p.prt(r)
