"""
Run AccTest slave on a dedicated test machine
"""

import socket
import os

from accTest import LOGGING
from accTest import networks
from accTest.applications import utilities

logger = LOGGING.getLogger(__name__)


class AccTestSlaveInvoker(object):
    """
    Send command to a running slave
    """

    def __init__(self, hostName, portNumber):
        self._hostName = hostName
        self._portNumber = portNumber

    def run(self, hostType, dslFileName):
        dslFilePath = utilities.getDslFilePath(dslFileName)
        s = socket.socket()
        s.connect((self._hostName, self._portNumber))
        args = "dslFilePath='{}'".format(dslFilePath)
        if hostType:
            args += ",hostType='{}'".format(hostType)
        else:
            args += ",hostType=''"
        s.send('command:runAccTest,{}'.format(args))
        s.close()
        del s


class AccTestSlave(object):

    def __init__(self, portNumber):
        self._slave = networks.Slave(portNumber)

    def run(self):
        self._slave.registerCommand('runAccTest', cmdRunAccTest)
        self._slave.run()


def cmdRunAccTest(slave, **kwargs):
    hostType = kwargs.get('hostType', '')
    dslFilePath = kwargs.get('dslFilePath')
    if not (dslFilePath and os.path.isfile(dslFilePath)):
        return False
    cls = utilities.getRunnerByTypeName(hostType)
    runner = cls()
    logger.info("{}.run('{}')".format(runner, dslFilePath))
    runner.run(dslFilePath)
    if runner.outFilePaths():
        utilities.publishResults(hostType, dslFilePath, runner.outFilePaths(), coverageFiles=runner.coverageFiles())
