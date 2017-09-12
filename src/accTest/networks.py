
import os
import socket
import stat
import time

from accTest import terminal

from accTest import LOGGING
logger = LOGGING.getLogger(__name__)


class PortFile(object):

    @staticmethod
    def getPath(name):
        return os.path.join('/tmp', name)

    def __init__(self, portNumber=9038):
        """

        Args:
            portNumber (int):
        """
        self._name = str(portNumber)
        self._path = self.getPath(self._name)

    def initialize(self):
        if os.path.isfile(self._path):
            os.remove(self._path)

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        fileContent = ''
        if exc_type is None and exc_val is None and exc_tb is None:
            fileContent = self._name
        with open(self._path, 'w') as fp:
            fp.write(fileContent)

    def path(self):
        return self._path

    def _exists(self):
        return os.path.exists(self._path)

    def _size(self):
        return os.stat(self._path)[stat.ST_SIZE]

    def wait(self, timeOut=30):
        """
        Waits for the creation of the port file
        Args:
            timeOut (int): optional

        Returns:
            bool: automatically calling _exists() on return
        """
        start_ = time.time()
        while True:
            if (time.time() - start_) >= timeOut:
                break
            if self._exists():
                return True
            time.sleep(0.5)
        return self._exists()

    def __nonzero__(self):
        return self._exists() and self._size() > 0


def cmdTerminate(slave, **kwargs):
    """

    Args:
        slave (Slave):

    Returns:
        bool:
    """
    slave.close()
    return False


class ConnectionManager(object):

    def __init__(self, portNumber):
        self._portNumber = portNumber
        self._s = socket.socket()
        self._s.bind((socket.gethostname(), self._portNumber))
        self._sockName = self._s.getsockname()
        self._s.listen(0xFF)
        self._sConnected = None

    def sockName(self):
        return self._sockName

    def waitForConnection(self):
        """
        Will block
        """
        terminal.printC('Waiting for connection (this: {})'.format(self._sockName), color='blue')
        result = self._s.accept()
        self._sConnected = result[0]

    def isConnected(self):
        return bool(self._sConnected)

    def disconnect(self):
        if self._sConnected:
            self._sConnected.close()
            self._sConnected = None

    def socket(self):
        return self._sConnected

    def terminate(self):
        self.disconnect()
        self._s.close()
        self._s = None

    def isTerminated(self):
        return self._s is None and self._sConnected is None


class Slave(object):

    def __init__(self, portNumber):
        self._connMan = ConnectionManager(portNumber)
        self._commands = dict()
        self.registerCommand('terminate', cmdTerminate)

    def _recv(self):
        return self._connMan.socket().recv(0xFF)

    def close(self):
        self._connMan.disconnect()
        terminal.printC('Slave has been closed.', color='blue')

    def registerCommand(self, name, func):
        """
        command is a free function whose signature is:

        bool = func(slave_obj, **kwargs)

        while running, slave will trap any text starts with "command:" keyword and dispatch the information to the
        corresponding command object(s)

        command:sendEmail, recipients=['a', 'b', 'c'], title='example'

        return True or None if slave should continue to run or wait, return False is slave must be closed

        Args:
            name (str):
            func (callable):

        Returns:
            bool: True if registered, False if ignored
        """
        self._commands[name] = func

    def _parseCommand(self, text):
        """

        Args:
            text (str):

        Returns:
            tuple: command object and its optional keyword arguments (dict)
        """
        cmdStr = text.split('command:')[-1]
        tokens = [tk.strip() for tk in cmdStr.split(',')]
        if len(tokens) < 1:
            return None, None
        cmdName = tokens[0]
        cmd_ = self._commands.get(cmdName)
        if not cmd_:
            return None, None
        keywordArgs = dict()
        for tk in tokens[1:]:
            lhs, rhs = tk.split('=')
            keywordArgs[lhs] = eval(rhs)
        return cmd_, keywordArgs

    def run(self):
        try:
            while not self._connMan.isTerminated():
                self._connMan.waitForConnection()
                terminal.printC('Connected with: {}'.format(self._connMan.sockName()), color='blue')
                self._run()
        except KeyboardInterrupt, e:
            pass
        except Exception, e:
            terminal.printC('critical error:\n{}'.format(str(e)), color='red')
        self.close()

    def _run(self):
        while self._connMan.isConnected():
            terminal.printC('Waiting for incoming data...', color='blue')
            textBuffer = self._recv().strip()

            if not textBuffer:
                terminal.printC('receive no data from recv(); is connection closed?', color='red')
                self._connMan.disconnect()
                break

            if not textBuffer.startswith('command:'):
                terminal.printC('{} (warning: not a command)'.format(textBuffer), color='yellow')
                continue

            cmd_, kwargs = self._parseCommand(textBuffer)
            if not cmd_:
                terminal.printC('{} (warning: not supported)'.format(textBuffer), color='yellow')
                continue

            ret_ = False
            try:
                terminal.printC('{} (running)'.format(textBuffer), color='white')
                ret_ = cmd_(self, **kwargs)
            except Exception, e:
                terminal.printC('Error: {}'.format(e), color='red')

            if ret_ is False:
                self._connMan.disconnect()
                break

            time.sleep(1)
