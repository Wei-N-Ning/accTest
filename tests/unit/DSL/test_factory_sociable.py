
import unittest

from accTest import exceptions
from accTest.DSL import factory

import mock


class TestFindTaskFile(unittest.TestCase):

    def test_givenNullPath_expectNullReturn(self):
        self.assertFalse(factory.findTaskFile('', ''))

    def test_givenNonExistingPath_expectNullReturn(self):
        self.assertFalse(factory.findTaskFile('/lol/foo', ''))

    def test_givenInvalidPath_expectNullReturn(self):
        with mock.patch('os.path.isfile', mock.MagicMock(return_value=False)):
            self.assertFalse(factory.findTaskFile('/invalid/path/Foo.py', 'Foo'))

    def test_givenValidPath_expectFullPath(self):
        with mock.patch('os.path.isfile', mock.MagicMock(return_value=True)):
            self.assertEqual('/valid/path/document/Foo.py',
                             factory.findTaskFile('/valid/path/document.py', 'Foo'))


class TestImportTaskModule(unittest.TestCase):

    def setUp(self):
        self.find_module_mock = mock.MagicMock()
        self.load_module_mock = mock.MagicMock()
        self.patcher = mock.patch.multiple(
            'imp',
            find_module=self.find_module_mock,
            load_module=self.load_module_mock)

    def test_failToFindModule_expectRaises(self):
        self.find_module_mock.side_effect = ImportError
        with self.patcher:
            self.assertRaises(exceptions.CanNotLoadTask,
                              factory.importPythonModule, '/non/existing/task.py')

    def test_failToLoadModule_expectRaises(self):
        self.find_module_mock.return_value = (mock.MagicMock(), mock.MagicMock(), mock.MagicMock())
        self.load_module_mock.side_effect = ImportError
        with self.patcher:
            self.assertRaises(exceptions.CanNotLoadTask,
                              factory.importPythonModule, '/an/existing/task.py')

    def test_expectModuleObjectReturned(self):
        mockModule = mock.MagicMock()
        self.find_module_mock.return_value = (mock.MagicMock(), mock.MagicMock(), mock.MagicMock())
        self.load_module_mock.return_value = mockModule
        with self.patcher:
            mod = factory.importPythonModule('/an/existing/task.py')
        self.assertEqual(mockModule, mod)


