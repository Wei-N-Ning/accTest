
import glob
import os
import shutil
import time


class PathGenerator(object):

    def __init__(self, source='$COVERAGE_FILE', target='/tmp/accTest.coverages'):
        self._source = source
        self._target = target

    def _pathOrVar(self, aString):
        if aString.startswith('$'):
            return os.environ.get(aString[1:], '')
        return aString

    def targetPattern(self):
        return '{}*'.format(self._pathOrVar(self._target))

    def targetPath(self):
        return '{}.{}'.format(self._pathOrVar(self._target), time.time())

    def sourcePath(self):
        return self._pathOrVar(self._source)


class CoverageFilesManager(object):

    def __init__(self, pathGenerator=None):
        self._pathGen = pathGenerator if pathGenerator else PathGenerator()

    def collect(self):
        return glob.glob(self._pathGen.targetPattern())

    def cleanSource(self):
        filePath = self._pathGen.sourcePath()
        if filePath and os.path.isfile(filePath):
            os.remove(filePath)

    def copySourceToTarget(self):
        filePath = self._pathGen.sourcePath()
        newFilePath = self._pathGen.targetPath()
        if filePath and os.path.isfile(filePath):
            shutil.copy(filePath, newFilePath)
