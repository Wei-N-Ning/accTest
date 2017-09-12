
import ctypes
import socket
import sys
import threading
import uuid
import weakref


class Screenplay(object):
    """
    Screenplay contains the staged scenarios where certain error, exceptional condition or fatal accident may happen.
    """

    def __init__(self):
        self._scenarios = list()
        self._attrs = dict()

    def setScenario(self, name, desciption):
        """
        Args:
            name (str):
            desciption (str):
        """
        class_ = _ScenarioRegistry.getClass(name)
        assert class_, 'Unsupported scenario: {}'.format(name)
        ins_ = class_(desciption, screenplay=self)
        self._scenarios.append(ins_)

    def setValue(self, key_, value_):
        self._attrs[key_] = value_

    def getValue(self, key_):
        return self._attrs.get(key_)

    def iter(self):
        """

        Returns:
            generator: an iterator that yields a scenario object at a time
        """
        return iter(self._scenarios)

    def write(self, filePath):
        with open(filePath, 'w') as fp:
            for scenario in self.iter():
                fp.write('{} {}\n'.format(scenario.name(), scenario.desc()))

    @classmethod
    def fromFile(cls, filePath):
        """
        A screenplay file is an ascii text file that contains one or more lines. Each line contains two words separated
         by one space, where the first word describes the scenario (such as pass, exception, segfault...) and the
          second describes the detail (such as the exception type, the exit code or a file to be created)

        A line that starts with # is skipped. You can use this feature to leave comments in the screenplay file.

        Args:
            filePath (str):

        Returns:
            Screenplay
        """
        with open(filePath, 'r') as fp:
            return cls.fromTextBuffer(fp.read())

    @classmethod
    def fromTextBuffer(cls, textBuffer):
        ins = cls()
        for eachLine in textBuffer.split('\n'):
            if len(eachLine) < 3:
                continue
            if eachLine.startswith('#'):
                continue
            tokens = eachLine.split(' ')
            if len(tokens) != 2:
                continue
            scenario = tokens[0].strip()
            description = tokens[1].strip()
            ins.setScenario(scenario, description)
        return ins


class Impersonator(object):
    """
    Impersonator plays a role that simulates the behavior of a real world application (maya, motion-builder etc...).

    Its acts are based on the screenplay.
    """

    def act(self, screenplay):
        """
        Args:
            screenplay (Screenplay):
        """
        for scenario in screenplay.iter():
            scenario.play()


class _ScenarioRegistry(type):
    _registry = dict()

    def __new__(mcs, clsName, *args):
        clsObj = type.__new__(mcs, clsName, *args)
        if clsObj.NAME:
            mcs._registry[clsObj.NAME] = clsObj
        return clsObj

    @classmethod
    def getClass(mcs, clsName):
        return mcs._registry.get(clsName, None)

    @classmethod
    def clear(mcs):
        mcs._registry.clear()


class Scenario(object):
    """
    Defines a scenario;

    Screenplay use the internal <name: class> mapping to find and instantiate each scenario class.
    """

    __metaclass__ = _ScenarioRegistry

    NAME = ''

    def __init__(self, description='', screenplay=None):
        self._description = description
        if screenplay:
            self._screenplay = weakref.ref(screenplay)
        else:
            self._screenplay = None

    def screenplay(self):
        if self._screenplay:
            return self._screenplay()
        return None

    def desc(self):
        return self._description

    def name(self):
        return self.NAME

    def play(self):
        pass


class SegFault(Scenario):
    """
    Causes segfault
    """

    NAME = 'segfault'

    def play(self):
        c_char = ctypes.c_char('a')
        c_p_char = ctypes.pointer(c_char)
        c_p_char[0xFFFFFFFF] = 'a'


class WriteToStdout(Scenario):
    """
    Write description to stdout
    """

    NAME = 'stdout'

    def play(self):
        sys.stdout.write(self.desc())


class WriteToStderr(Scenario):
    """
    Write description to stderr
    """

    NAME = 'stderr'

    def play(self):
        sys.stderr.write(self.desc())


class Exit(Scenario):
    """
    Causes normal process termination; the description must be convertible to a BYTE
    """

    NAME = 'exit'

    def play(self):
        sys.exit(int(self.desc()))


class CreateRandomFile(Scenario):
    """
    Create a file with random bytes; the file path is specified by description
    """

    NAME = 'randomfile'

    def play(self):
        filePath = self.desc()
        with open(filePath, 'w') as fp:
            fp.write(uuid.uuid4().bytes)


class PortOpen(Scenario):
    """
    Open a port specified by description. It does not check whether the port is in use. If port is 0 it will randomly
    pick a free port (recommended)

    Description must use one of these formats:
    hostname:port (e.g. 127.0.0.1:8080)
    port (e.g. 8080)

    Will populate the following attributes on the screenplay object:

    hostName: str
    portNumber: int
    socket: a socket object (the one that listens)
    """

    NAME = 'portopen'

    def play(self):
        tokens = self.desc().split(':')
        if len(tokens) == 2:
            hostName = tokens[0]
            portNumber = int(tokens[1])
        elif len(tokens) == 1:
            hostName = '127.0.0.1'
            portNumber = int(tokens[0])
        else:
            hostName = '127.0.0.1'
            portNumber = 0
        s = socket.socket()
        s.bind((hostName, portNumber))
        s.listen(100)
        server, client = s.accept()
        sp = self.screenplay()
        sp.setValue('socket', server)
        sp.setValue('hostName', hostName)
        sp.setValue('portNumber', portNumber)


class Wait(Scenario):
    """
    Forces the process to wait/sleep for a given amount of time, specified by description in seconds

    Description must be convertible to a float
    """

    NAME = 'wait'

    def play(self):
        event_ = threading.Event()
        event_.wait(float(self.desc()))


class SetAttribute(Scenario):
    """
    Set an attribute; try to avoid using this at all costs

    The description must separate the attribute and its value by a colon, e.g.
    key:value
    """

    NAME = 'setattr'

    def play(self):
        attrName, attrValue = self.desc().split(':')
        sp = self.screenplay()
        sp.setValue(attrName, attrValue)


class FakePython(Impersonator):

    def act(self, screenplay):
        for scenario in screenplay.iter():
            scenario.play()
