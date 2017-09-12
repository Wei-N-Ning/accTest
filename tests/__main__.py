
import os
import sys

from moTest import finder
from moTest import coverages


def runUnitTests():
    return finder.runTestsInDir(os.path.join(os.path.dirname(__file__), 'unit'))


def runIntegrationTests():
    return finder.runTestsInDir(os.path.join(os.path.dirname(__file__), 'integration'))


def run():
    cov = coverages.CoverageRAII(source=['accTest'], cleanUp=False, reportOnDelete=True)
    if len(sys.argv) > 1 and sys.argv[1] == 'i':
        return runIntegrationTests()
    if len(sys.argv) > 1 and sys.argv[1] == 'a':
        return runUnitTests() and runIntegrationTests()
    return runUnitTests()


if __name__ == '__main__':
    sys.exit(0 if run() else 1)
