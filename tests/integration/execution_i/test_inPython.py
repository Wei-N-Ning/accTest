
import unittest

from accTest import resources
from accTest.execution import inPython

import testdata


class TestRunInPython_Fatal(unittest.TestCase):

    def setUp(self):
        self.dslExample = resources.filePath('dslExample.py')

    def test_segFault(self):
        runner = inPython.RunInPython(pythonExe=testdata.filePath('python_segfault'))
        runner.run(self.dslExample)

    def test_exit_nonzero(self):
        runner = inPython.RunInPython(pythonExe=testdata.filePath('python_exit_nonzero'))
        runner.run(self.dslExample)

    def test_broken_results(self):
        runner = inPython.RunInPython(pythonExe=testdata.filePath('python_broken_results'))
        runner.run(self.dslExample)


if __name__ == '__main__':
    unittest.main()
