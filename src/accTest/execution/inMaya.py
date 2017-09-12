import os
import socket
import time

from accTest import DSL
from accTest import LOGGING
from accTest import networks
from accTest import terminal
from accTest.execution import interfaces
from accTest.execution.IOUtilities import coverageFiles
from accTest.execution.IOUtilities import ozEnv
from accTest.execution.IOUtilities import resultFiles
from accTest.objectModel import result as _result
from moTest import coverages

logger = LOGGING.getLogger(__name__)


def init(port):
    """
    Args:
        port (int):
    """

    portFile = networks.PortFile(port)
    portFile.initialize()
    with portFile:
        from maya import cmds
        cmds.commandPort(name=':{}'.format(port), sourceType='python', returnNumCommands=True)


def createCov(fixtures):
    if not coverages.Coverage:
        return None
    if not fixtures:
        return None
    listOfSources = fixtures[0].getValue('coverages')
    if listOfSources and isinstance(listOfSources, list):
        return coverages.Coverage(source=listOfSources)
    if fixtures[0].getValue('enableCoverage') is True:
        return coverages.Coverage()


def execute(dslFilePath, indexes, outFilePath):
    fixtures = DSL.parse(dslFilePath, instantiation=True, indexes=indexes)
    results = []
    cov = createCov(fixtures)
    if cov:
        cov.start()
    logger.info('Proceed to execute fixtures')
    logger.info('dsl: {}'.format(dslFilePath))
    logger.info('indexes: {}'.format(indexes))
    logger.info('outFilePath: {}'.format(outFilePath))
    for fixture in fixtures:
        for task in fixture.iterTasks():
            results.append(task.run())
    _result.write(results, outFilePath)
    if cov:
        cov.stop()
        cov.save()


class RunInMayaGui(interfaces.RunnerInterface):

    DEFAULT_PORT = 9038
    DEFAULT_LOCALHOST = '127.0.0.1'
    DEFAULT_MAYA_EXE = 'maya'

    def __init__(self, mayaExe=None, portNumber=None, showResultDetails=True):
        self._mayaExe = mayaExe if mayaExe else self.DEFAULT_MAYA_EXE
        self._portNumber = portNumber if portNumber is not None else self.DEFAULT_PORT
        self._portFile = None
        self._showResultDetails = showResultDetails
        self._resultFilesManager = resultFiles.ResultFilesManager('/tmp/mayatestresults.{}')
        self._covFilesManager = coverageFiles.CoverageFilesManager()
        self._resultFilesManager.resetOutFiles()

    def coverageFiles(self):
        return self._covFilesManager.collect()

    def outFilePaths(self):
        return self._resultFilesManager.paths()

    def outFilePath(self, create=False):
        return self._resultFilesManager.outFilePath(create=create)

    def run(self, dslFilePath):
        fixtures = DSL.parse(dslFilePath, instantiation=False)
        fixtureIndexesByEnv = ozEnv.fixtureIndexesByEnv(fixtures)
        for env_, indexes in fixtureIndexesByEnv.iteritems():
            self._covFilesManager.cleanSource()
            self._setUpPortFile()
            p, s = self._initialize(env_)
            retCode = self._run(p, s, dslFilePath, indexes)
            if retCode is None:
                retCode = self._deinitialize(p, s)
            if retCode == 0:
                self._postRun(p)
            else:
                self._postErrorHandling(p)
            self._tearDownPortFile()
            self._covFilesManager.copySourceToTarget()

    def debug(self, dslFilePath):
        fixtures = DSL.parse(dslFilePath, instantiation=False)
        fixtureIndexesByEnv = ozEnv.fixtureIndexesByEnv(fixtures)
        for env_, indexes in fixtureIndexesByEnv.iteritems():
            terminal.printC('Oz command', color='yellow')
            terminal.printC(env_.createOzCmdLineOnly(), color='white')
            terminal.printC('Initialize Maya command port', color='yellow')
            terminal.printC(self._createInitCmd(), color='white')
            terminal.printC('Execute...', color='yellow')
            terminal.printC(self._createCmd(dslFilePath, indexes, createOutputFile=True), color='white')

    def _createInitCmd(self):
        cmd_ = """{} -command 'python("from accTest.execution import inMaya as m; m.init({})")'""".format(
            self._mayaExe, self._portNumber
        )
        return cmd_

    def _setUpPortFile(self):
        self._portFile = networks.PortFile(self._portNumber)

    def _tearDownPortFile(self):
        self._portFile = None
        self._portNumber += 1

    def _initialize(self, env_):
        """

        Args:
            env_ (ozEnv.OzEnv):

        Returns:
            tuple: (subprocess.Popen, socket.socket)
        """
        initCmd = self._createInitCmd()
        p = env_.createProcess(initCmd)
        assert self._portFile.wait(timeOut=120), 'Failed to initialize!!!'
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                s.connect((self.DEFAULT_LOCALHOST, self._portNumber))
                break
            except socket.error, e:
                time.sleep(0.5)
        return p, s

    def _createCmd(self, dslFilePath, indexes, createOutputFile=True):
        cmd_ = "from accTest.execution import inMaya as m; m.execute('{}', {}, '{}')".format(
            dslFilePath, indexes, self.outFilePath(create=createOutputFile)
        )
        return cmd_

    def _run(self, p, s, dslFilePath, indexes):
        cmd_ = self._createCmd(dslFilePath, indexes)
        logger.info('Sending command line to Maya')
        logger.info(cmd_)
        s.send(cmd_)
        retCode = p.poll()
        while retCode is None:
            if os.path.isfile(self.outFilePath()):
                break
            time.sleep(0.5)
            retCode = p.poll()
        return retCode

    def _deinitialize(self, p, s):
        s.send("from maya import cmds; cmds.quit(f=True)")
        retCode = p.poll()
        while retCode is None:
            time.sleep(0.5)
            retCode = p.poll()
        return retCode

    def _postRun(self, p):
        rList = _result.read(self.outFilePath())
        if rList:
            _result.prt(rList, includeDetails=self._showResultDetails)
        else:
            err = p.stderr.read()
            terminal.printC('Broken results: {}'.format(self.outFilePath()), color='red')
            terminal.printC('stderr:\n', color='red')
            terminal.printC(err, color='red')

    def _postErrorHandling(self, p):
        terminal.printC('Process exits with non-zero return code', color='red')
        err = p.stderr.read()
        if err:
            terminal.printC('stderr:\n', color='red')
            terminal.printC(err, color='red')
