
import unittest

from accTest.execution.IOUtilities import resultFiles

from moTest.patches import monkey
import mock


class TestResultFilesManager(unittest.TestCase):

    def setUp(self):
        self.globStub = mock.MagicMock()
        self.osStub = mock.MagicMock()
        self.monkey = monkey.PatcherFactory()
        self.monkey.patch(resultFiles, 'os', self.osStub)
        self.monkey.patch(resultFiles.glob, 'glob', self.globStub)

    def tearDown(self):
        self.monkey.unpatchAll()

    def test_resetOutFiles_expectCalled(self):
        self.globStub.return_value = ['aa']
        rfm = resultFiles.ResultFilesManager('e1m1{}')
        rfm.resetOutFiles()
        self.assertEqual('aa', self.osStub.remove.call_args[0][0])

    def test_getResultFilePath_expectRaisesIfNoFileAvailable(self):
        rfm = resultFiles.ResultFilesManager('e1m1{}')
        self.assertRaises(ValueError, rfm.outFilePath)

    def test_createResultFilePath_expectPaths(self):
        rfm = resultFiles.ResultFilesManager('e1m1{}')
        rfm.outFilePath(create=True)
        rfm.outFilePath(create=True)
        rfm.outFilePath(create=True)
        self.assertEqual('e1m12', rfm.outFilePath())
        self.assertEqual(['e1m10', 'e1m11', 'e1m12'], rfm.paths())

    def test_resetOutFiles_expectPathsCleaned(self):
        rfm = resultFiles.ResultFilesManager('e1m1{}')
        rfm.outFilePath(create=True)
        rfm.outFilePath(create=True)
        rfm.outFilePath(create=True)
        rfm.resetOutFiles()
        self.assertFalse(rfm.paths())
