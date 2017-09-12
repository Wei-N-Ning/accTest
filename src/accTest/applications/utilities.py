
import bisect
import os
import pwd
import shutil
import socket
import stat
import time

from accTest import constants
from accTest import LOGGING
from accTest.execution import inPython
from accTest.execution import inMaya
from accTest.execution import inMotionBuilder

from coverage import Coverage
from coverage import CoverageData

logger = LOGGING.getLogger(__name__)


def getDslFilePath(dslFileName):
    if not dslFileName.endswith('.py'):
        dslFileName += '.py'
    return os.path.abspath(os.path.join('.', dslFileName))


def getRunnerByTypeName(typeName):
    typeNameLower = typeName.lower()
    if typeNameLower in ('python', 'py', '', None):
        return inPython.RunInPython
    elif typeNameLower in ('mayapy', ):
        return inPython.RunInMayaPy
    elif typeNameLower in ('maya', ):
        return inMaya.RunInMayaGui
    elif typeNameLower in ('motionbuilder', 'mobu'):
        return inMotionBuilder.RunInMotionBuilderGui
    raise ValueError('Unsupported runner type: {}'.format(typeName))


class ResultPublisher(object):

    def getName(self):
        timeStamp = time.strftime('%Y%m%d_%H%M%S', time.localtime())
        hostName = socket.gethostname()
        ip_ = socket.gethostbyname(hostName)
        return '{}_{}_{}'.format(timeStamp, hostName, ip_)

    def getPath(self):
        return os.path.join(constants.TEST_RESULT_PUBLISH_PATH, self.getName())

    def publish(self, hostType, dslFilePath, resultFiles, coverageFiles=None):
        dirPath = self.getPath()
        os.mkdir(dirPath)
        runnerFilePath = os.path.join(dirPath, 'runner')
        with open(runnerFilePath, 'w') as fp:
            fp.write('hostType: {}\n'.format(hostType))
            fp.write('dslFilePath: {}\n'.format(dslFilePath))
        for resultFile in resultFiles:
            filePath_ = os.path.join(dirPath, os.path.basename(resultFile))
            shutil.copy(resultFile, filePath_)
            os.remove(resultFile)
        if coverageFiles:
            for path_ in coverageFiles:
                filePath_ = os.path.join(dirPath, os.path.basename(path_))
                shutil.copy(path_, filePath_)
                os.remove(path_)


class ResultWrangler(object):

    def getCoverageFile(self, namePattern):
        """
        Returns the first coverage file whose name matches with the given pattern

        Args:
            namePattern (str):

        Returns:
            str:
        """
        for dir_, dirNames, fileNames in os.walk(constants.TEST_RESULT_PUBLISH_PATH):
            if namePattern in fileNames:
                return os.path.join(os.path.abspath(dir_), namePattern)
        return ''

    def iterCoverageFile(self):
        for dir_, dirNames, fileNames in os.walk(constants.TEST_RESULT_PUBLISH_PATH):
            for fileName in fileNames:
                if fileName.startswith('accTest.coverages'):
                    yield os.path.join(os.path.abspath(dir_), fileName)

    def aggregateResults(self, fileNames, outFilePath='/tmp/.aggregated.coverage'):
        masterCovData = CoverageData()
        for fileName in fileNames:
            filePath = self.getCoverageFile(fileName)
            if filePath:
                covData = CoverageData()
                covData.read_file(filePath)
                masterCovData.update(covData)
        masterCovData.write_file(outFilePath)
        return outFilePath


def reporterByFlavor(flavor=''):
    if flavor:
        if flavor.lower() == 'anim':
            return CoverageReporterAnim()
        else:
            logger.error('Can not find reporter from flavor: {}'.format(flavor))
    return CoverageReporterDefault()


class CoverageReporterDefault(object):

    def report(self, filePath):
        cov = Coverage(data_file=filePath)
        cov.load()
        cov.report()


class CoverageReporterAnim(object):

    def report(self, filePath):
        cov = Coverage(data_file=filePath)
        cov.load()
        # mocore
        cov.report(include=['*/core/*'])
        # molibs
        cov.report(include=['*/libs/*'])
        # motils
        cov.report(include=['*/utils/*'])


def reportCoverage(fileNames, flavor=None):
    if fileNames:
        filePath = ResultWrangler().aggregateResults(fileNames)
    else:
        filePath = os.environ.get('COVERAGE_FILE', '/tmp/.coverage')
    if not (filePath and os.path.isfile(filePath)):
        return
    reporter = reporterByFlavor(flavor=flavor)
    reporter.report(filePath)


def listCoverage(stats=None):
    if not stats:
        stats = {'size': stat.ST_SIZE, 'm_time': stat.ST_MTIME, 'user': stat.ST_UID}
    print 'file name'.ljust(40), ''.join([k.ljust(24) for k, v in stats.iteritems()])
    filePaths = []
    for filePath in ResultWrangler().iterCoverageFile():
        bisect.insort(filePaths, filePath)
    for filePath in filePaths:
        fileName = os.path.basename(filePath)
        sd = statsDict(stats, filePath)
        statString = ''.join([v.ljust(24) for k, v in sd.iteritems()])
        print fileName.ljust(40), statString


def statsDict(stats, filePath):
    statStruct = os.stat(filePath)
    dictToReturn = dict()
    for statName in sorted(stats.keys()):
        statField = stats[statName]
        value = statStruct[statField]
        if statField in (stat.ST_ATIME, stat.ST_CTIME, stat.ST_MTIME):
            dictToReturn[statName] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(value))
        elif statField == stat.ST_SIZE:
            dictToReturn[statName] = '{}K'.format(round(value / 1024.0, 2))
        elif statField == stat.ST_UID:
            dictToReturn[statName] = pwd.getpwuid(statStruct[stat.ST_UID])[4]
        else:
            dictToReturn[statName] = str(value)
    return dictToReturn


def publishResults(hostType, dslFilePath, resultFiles, coverageFiles=None):
    ResultPublisher().publish(hostType, dslFilePath, resultFiles, coverageFiles=coverageFiles)
