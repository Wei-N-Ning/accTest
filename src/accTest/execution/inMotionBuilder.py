
import os
import tempfile
import time
import sys

from accTest import DSL
from accTest import LOGGING
from accTest import terminal
from accTest.execution import interfaces
from accTest.execution.IOUtilities import coverageFiles
from accTest.execution.IOUtilities import outputs
from accTest.execution.IOUtilities import ozEnv
from accTest.execution.IOUtilities import resultFiles
from accTest.objectModel import result as _result

from moTest import coverages

logger = LOGGING.getLogger(__name__)


def createCov(fixtures):
    filePath = os.environ.get('COVERAGE_FILE', '.coverage')
    absFilePath = os.path.abspath(filePath)
    if absFilePath and os.path.isfile(absFilePath):
        os.remove(absFilePath)
    if not coverages.Coverage:
        return None
    if not fixtures:
        return None
    listOfSources = fixtures[0].getValue('coverages')
    if listOfSources and isinstance(listOfSources, list):
        return coverages.Coverage(source=listOfSources)
    if fixtures[0].getValue('enableCoverage') is True:
        return coverages.Coverage()


def execute(dslFilePath, indexes, outFilePath, outFile, errFile):
    outputs.initializeOutputRedirection(outFile, errFile)
    results = []
    try:
        fixtures = DSL.parse(dslFilePath, instantiation=True, indexes=indexes)
        cov = createCov(fixtures)
        if cov:
            cov.start()
        for fixture in fixtures:
            for task in fixture.iterTasks():
                results.append(task.run())
        _result.write(results, outFilePath)
        if cov:
            cov.stop()
            cov.save()
    except Exception, e:
        sys.stderr.write('{}\n'.format(e))
    finally:
        outputs.finalizeOutputRedirection()


class RunInMotionBuilderGui(interfaces.RunnerInterface):

    DEFAULT_PORT = 4242
    DEFAULT_LOCALHOST = '127.0.0.1'
    DEFAULT_MOTIONBUILDER_EXE = 'motionbuilder'

    def __init__(self, motionbuilderExe=None, host=None, portNumber=None, showResultDetails=True):
        self._motionBuilderExe = motionbuilderExe if motionbuilderExe is not None else self.DEFAULT_MOTIONBUILDER_EXE
        self._host = host if host is not None else self.DEFAULT_LOCALHOST
        self._portNumber = portNumber if portNumber is not None else self.DEFAULT_PORT
        self._showResultDetails = showResultDetails
        self._resultFilesManager = resultFiles.ResultFilesManager('/tmp/motionbuildertestresults.{}')
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
        if not fixtures:
            return
        fixtureIndexesByEnv = ozEnv.fixtureIndexesByEnv(fixtures)
        for env_, indexes in fixtureIndexesByEnv.iteritems():
            scriptFile = self._createScriptFile(dslFilePath, indexes)
            cmd = '{} -suspendMessages {}'.format(self._motionBuilderExe, scriptFile)
            p = env_.createProcess(cmd)
            retCode = p.poll()
            while retCode is None:
                time.sleep(0.5)
                retCode = p.poll()
            if retCode == 0:
                self._postRun(p)
            else:
                self._postErrorHandling(p, retCode)
            self._covFilesManager.copySourceToTarget()

    def _createScriptFile(self, dslFilePath, indexes):
        text = \
"""
from accTest.execution import inMotionBuilder as m
m.execute('{}', {}, '{}', '{}', '{}')
import pyfbsdk
pyfbsdk.FBApplication().FileExit()
"""
        text = text.format(dslFilePath, indexes, self.outFilePath(create=True), '/tmp/stdout.txt', '/tmp/stderr.txt')
        _, filePath = tempfile.mkstemp(prefix='AccMobu_', suffix='.py')
        with open(filePath, 'w') as fp:
            fp.write(text)
        return filePath

    def _postRun(self, p):
        rList = _result.read(self.outFilePath())
        if rList:
            _result.prt(rList, includeDetails=self._showResultDetails)
        else:
            terminal.printC('Broken results: {}'.format(self.outFilePath()), color='red')
            printOutputs(p)

    def _postErrorHandling(self, p, retCode):
        terminal.printC('Process exits with non-zero return code: {}'.format(retCode), color='red')
        printOutputs(p)


def printOutputs(process):
    terminal.printC('======== motionbuilder outputs ========\n', color='white')
    err = process.stderr.read()
    terminal.printC('stderr:\n', color='red')
    terminal.printC(err, color='red')
    out = process.stdout.read()
    terminal.printC('stdout:\n', color='yellow')
    terminal.printC(out, color='yellow')

    terminal.printC('======== python outputs ========\n', color='white')
    with open('/tmp/stderr.txt', 'r') as fp:
        err = fp.read()
    terminal.printC('stderr:\n', color='red')
    terminal.printC(err, color='red')
    with open('/tmp/stdout.txt', 'r') as fp:
        out = fp.read()
    terminal.printC('stdout:\n', color='yellow')
    terminal.printC(out, color='yellow')

