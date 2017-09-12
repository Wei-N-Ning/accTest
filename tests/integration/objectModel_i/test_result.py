
import unittest

from fileSysUtils import fileSystem

from accTest.objectModel import result

import mock


class TestSerializer(unittest.TestCase):

    def setUp(self):
        self.tempFile = fileSystem.TempFile(prefix='AccTestObjectModelResult', suffix='.json')
        self.path = self.tempFile.filePath
        self.s = result.Serializer()
        self.results = [
            result.Result('testOne', True, 'success'),
            result.Result('testTwo', False, 'fail!!'),
            result.Result('testThree', False, 'Exception!!!!')
        ]

    def tearDown(self):
        self.tempFile = None

    def test_writeOne_readOne(self):
        self.s.write(self.results[0], self.path)
        results = self.s.read(self.path)
        self.assertEqual(1, len(results))
        self.assertEqual(self.results[0].__dict__, results[0].__dict__)

    def test_writeAll_readAll(self):
        self.s.write(self.results, self.path)
        results = self.s.read(self.path)
        self.assertEqual(3, len(results))
        self.assertEqual(self.results[0].__dict__, results[0].__dict__)
        self.assertEqual(self.results[1].__dict__, results[1].__dict__)
        self.assertEqual(self.results[2].__dict__, results[2].__dict__)


class TestPrinter(unittest.TestCase):

    def setUp(self):
        self.results = [
            result.Result('testOne', True, 'success'),
            result.Result('testTwo', False, 'fail!!'),
            result.Result('testThree', False, 'Exception!!!!')
        ]

    def test_useShell(self):
        p = result.Printer()
        p.prt(self.results[0])
        p.prt(self.results[1])
        p.prt(self.results[2])

    def test_useOutputStream(self):
        oStream = mock.MagicMock()
        oStream.write = mock.MagicMock()
        p = result.Printer(oStream=oStream)
        p.prt(self.results[0])
        p.prt(self.results[1])
        p.prt(self.results[2])
        self.assertTrue(oStream.write.call_count)


if __name__ == '__main__':
    unittest.main()
