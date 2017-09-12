
import os

from accTest.applications import utilities
from accTest import LOGGING

logger = LOGGING.getLogger(__name__)


class AccTestStandalone(object):

    def __init__(self, hostType, dslFileName):
        self._dslFilePath = utilities.getDslFilePath(dslFileName)
        self._hostType = hostType

    def run(self):
        cls = utilities.getRunnerByTypeName(self._hostType)
        runner = cls()
        logger.info("{}.run('{}')".format(runner, self._dslFilePath))
        runner.run(self._dslFilePath)
        if runner.outFilePaths():
            utilities.publishResults(self._hostType, self._dslFilePath, runner.outFilePaths(),
                                     coverageFiles=runner.coverageFiles())

    def debug(self):
        cls = utilities.getRunnerByTypeName(self._hostType)
        runner = cls()
        runner.debug(self._dslFilePath)
