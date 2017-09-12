
import os


def filePath(fileName):
    return os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        fileName
    )
