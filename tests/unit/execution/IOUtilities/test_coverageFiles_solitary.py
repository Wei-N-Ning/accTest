
import unittest

from accTest.execution.IOUtilities import coverageFiles

from moTest.patches import monkey
import mock


class TestPathGenerator(unittest.TestCase):

    def setUp(self):
        self.timeStub = mock.MagicMock(return_value=123.456)
        self.environStub = dict()
        self.monkey = monkey.PatcherFactory()
        self.monkey.patch(coverageFiles.time, 'time', self.timeStub)
        self.monkey.patch(coverageFiles.os, 'environ', self.environStub)

    def tearDown(self):
        self.monkey.unpatchAll()

    def test_emptySourceAndTarget_expectValues(self):
        pg = coverageFiles.PathGenerator(source='', target='')
        self.assertEqual('', pg.sourcePath())
        self.assertEqual('*', pg.targetPattern())
        self.assertEqual('.123.456', pg.targetPath())

    def test_givenEnvVar_expectExpansion(self):
        self.environStub['SOURCE'] = 'e1m1'
        self.environStub['TARGET'] = 'e3m3'
        pg = coverageFiles.PathGenerator(source='$SOURCE', target='$TARGET')
        self.assertEqual('e1m1', pg.sourcePath())
        self.assertEqual('e3m3*', pg.targetPattern())
        self.assertEqual('e3m3.123.456', pg.targetPath())


class TestCoverageFilesManager(unittest.TestCase):

    def setUp(self):
        self.pathGen = mock.MagicMock()
        self.osStub = mock.MagicMock()
        self.shutilStub = mock.MagicMock()
        self.globStub = mock.MagicMock()
        self.monkey = monkey.PatcherFactory()
        self.monkey.patch(coverageFiles, 'os', self.osStub)
        self.monkey.patch(coverageFiles.glob, 'glob', self.globStub)
        self.monkey.patch(coverageFiles, 'shutil', self.shutilStub)
        self.cfm = coverageFiles.CoverageFilesManager(pathGenerator=self.pathGen)

    def tearDown(self):
        self.monkey.unpatchAll()

    def test_collectCoverageFiles_expectPaths(self):
        self.globStub.return_value = ['aa']
        self.assertEqual(['aa'], self.cfm.collect())

    def test_cleanSource_expectCalled(self):
        self.osStub.path.isfile.return_value = True
        self.pathGen.sourcePath.return_value = '/doom/e1m1.coverages'
        self.cfm.cleanSource()
        self.assertEqual('/doom/e1m1.coverages', self.osStub.remove.call_args[0][0])

    def test_copySourceToTarget_expectCalled(self):
        self.osStub.path.isfile.return_value = True
        self.pathGen.sourcePath.return_value = '/doom/e1m1.coverages'
        self.pathGen.targetPath.return_value = '/doom/e3m3.coverages'
        self.cfm.copySourceToTarget()
        self.assertEqual('/doom/e1m1.coverages', self.shutilStub.copy.call_args[0][0])
        self.assertEqual('/doom/e3m3.coverages', self.shutilStub.copy.call_args[0][1])

