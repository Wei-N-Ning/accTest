
import unittest

from accTest import resources
from accTest.objectModel import fixture
from accTest.execution import inMaya

from moTest.patches import monkey
import mock


class TestRunInMayaGui(unittest.TestCase):

    def setUp(self):
        self.parseStub = mock.MagicMock(return_value=list())
        self.monkey = monkey.PatcherFactory()
        self.monkey.patch(inMaya.DSL, 'parse', self.parseStub)

    def tearDown(self):
        self.monkey.unpatchAll()

    def test_initialState(self):
        runner = inMaya.RunInMayaGui()
        self.assertFalse(runner.coverageFiles())
        self.assertFalse(runner.outFilePaths())

    def test_debug_expectNoFixtures(self):
        runner = inMaya.RunInMayaGui()
        runner.debug('/aaa/fixture.py')
