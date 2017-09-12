
import logging

from accTest import resources
from accTest.execution import inMaya


if __name__ == '__main__':
    logging.basicConfig()
    logging.root.setLevel(logging.INFO)
    dslFilePath = resources.filePath('dslExample.py')
    runner = inMaya.RunInMayaGui()
    runner.run(dslFilePath)
