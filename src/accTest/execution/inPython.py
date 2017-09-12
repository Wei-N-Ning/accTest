import logging
import time

from accTest import DSL
from accTest import terminal
from accTest.execution import interfaces
from accTest.execution.IOUtilities import coverageFiles
from accTest.execution.IOUtilities import ozEnv
from accTest.execution.IOUtilities import resultFiles
from accTest.objectModel import result as _result
from moTest import coverages

logger = logging.getLogger(__name__)


class RunInPython(interfaces.RunnerInterface):

    DEFAULT_PYTHON_EXE = 'python'

    def __init__(self, pythonExe=None, timeout=None, showResultDetails=True):
        self._pythonExe = pythonExe if pythonExe else self.DEFAULT_PYTHON_EXE
        self._timeout = timeout
        self._showResultDetails = showResultDetails
        self._resultFilesManager = resultFiles.ResultFilesManager('/tmp/testresults.{}')
        self._covFilesManager = coverageFiles.CoverageFilesManager()
        self._resultFilesManager.resetOutFiles()

    def coverageFiles(self):
        return self._covFilesManager.collect()

    def outFilePaths(self):
        return self._resultFilesManager.paths()

    def run(self, dslFilePath):
        fixtures = DSL.parse(dslFilePath, instantiation=False)
        fixtureIndexesByEnv = ozEnv.fixtureIndexesByEnv(fixtures)
        for env_, indexes in fixtureIndexesByEnv.iteritems():
            self._covFilesManager.cleanSource()
            self._run(env_, dslFilePath, indexes)
            self._covFilesManager.copySourceToTarget()

    def debug(self, dslFilePath):
        fixtures = DSL.parse(dslFilePath, instantiation=False)
        fixtureIndexesByEnv = ozEnv.fixtureIndexesByEnv(fixtures)
        for env_, indexes in fixtureIndexesByEnv.iteritems():
            cmd_ = self._createCmd(dslFilePath, indexes, createOutputFile=True)
            terminal.printC('Oz command', color='yellow')
            terminal.printC(env_.createOzCmdLineOnly(), color='white')
            terminal.printC('Command to execute:', color='yellow')
            terminal.printC(cmd_, color='white')

    def _createPythonCmdTemplate(self):
        cmd_ = self._pythonExe + ''' -c "from accTest.execution import inPython as m; m.run('{}', '{}', {})"'''
        return cmd_

    def _createCmd(self, dslFilePath, indexes, createOutputFile=True):
        cmd_ = self._createPythonCmdTemplate()
        cmd_ = cmd_.format(dslFilePath,
                           self._resultFilesManager.outFilePath(create=createOutputFile),
                           indexes)
        return cmd_

    def _run(self, env_, dslFilePath, indexes):
        """
        Args:
            env_ (ozEnv.OzEnv):
            dslFilePath (str):
            indexes (list):
        """
        cmd_ = self._createCmd(dslFilePath, indexes, createOutputFile=True)
        p = env_.createProcess(cmd_)
        retCode = self._wait(p, timeout=self._timeout)
        if retCode == 0:
            self._postRun(p)
        elif retCode is None:
            p.terminate()
            self._postErrorHandling(p, 'Process is timed out')
        else:
            self._postErrorHandling(p, 'Process exits with non-zero return code')

    def _wait(self, p, timeout=None):
        start_ = time.time()
        retCode = p.poll()
        while retCode is None:
            time.sleep(0.5)
            if timeout and (time.time() - start_) > timeout:
                break
            retCode = p.poll()
        return retCode

    def _postRun(self, p):
        resultFilePath = self._resultFilesManager.outFilePath()
        rList = _result.read(resultFilePath)
        if rList:
            _result.prt(rList, includeDetails=self._showResultDetails)
        else:
            err = p.stderr.read()
            terminal.printC('Broken results: {}'.format(resultFilePath), color='red')
            terminal.printC('stderr:\n', color='red')
            terminal.printC(err, color='red')

    def _postErrorHandling(self, p, msg):
        terminal.printC(msg, color='red')
        err = p.stderr.read()
        if err:
            terminal.printC('stderr:\n', color='red')
            terminal.printC(err, color='red')


class RunInMayaPy(RunInPython):

    DEFAULT_PYTHON_EXE = 'mayapy'

    def _createPythonCmdTemplate(self):
        cmd_ = self._pythonExe + ''' -c "from maya import standalone; standalone.initialize(); ''' + \
               '''from accTest.execution import inPython as m; m.run('{}', '{}', {})"'''
        return cmd_


def run(dslFilePath, outFilePath, listOfIndexes):
    fixtures = DSL.parse(dslFilePath, indexes=listOfIndexes, instantiation=True)
    if fixtures:
        listOfSources = fixtures[0].getValue('coverages')
        if listOfSources and isinstance(listOfSources, list):
            cov = coverages.CoverageRAII(source=listOfSources, cleanUp=False, reportOnDelete=False)
        elif fixtures[0].getValue('enableCoverage') is True:
            cov = coverages.CoverageRAII(cleanUp=False, reportOnDelete=False)
    results = []
    for fixture in fixtures:
        for task in fixture.iterTasks():
            results.append(task.run())
    _result.write(results, outFilePath)
