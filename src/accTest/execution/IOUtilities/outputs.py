
import sys


def initializeOutputRedirection(outFile, errFile):
    """
    Redirect the output (stdout, stderr) of the CURRENT process to the given files

    Args:
        outFile (str):
        errFile (str):
    """

    sys.stdout = open(outFile, 'w')
    sys.stderr = open(errFile, 'w')


def finalizeOutputRedirection():
    sys.stdout.flush()
    sys.stdout.close()
    sys.stderr.flush()
    sys.stderr.close()
