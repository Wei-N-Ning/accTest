
import os
import stat
import unittest

from accTest import networks

import mock


class TestPortFile(unittest.TestCase):

    def setUp(self):
        self._tempFiles = []
        self._portName = 'woodhead'
        self._pf = networks.PortFile(self._portName)
        self._pf.initialize()
        self._tempFiles.append(self._pf.path())

    def tearDown(self):
        for filePath in self._tempFiles:
            if os.path.isfile(filePath):
                os.remove(filePath)

    def test_expectInitialFalseState(self):
        self.assertFalse(self._pf)

    def test_noException_expectPortFileCreated(self):
        with self._pf:
            pass
        self.assertTrue(os.path.isfile(self._pf.path()))

    def test_noException_expectPortFileSize(self):
        with self._pf:
            pass
        statDict = os.stat(self._pf.path())
        self.assertEqual(len(self._portName), statDict[stat.ST_SIZE])

    def test_noException_expectPostState(self):
        with self._pf:
            pass
        self.assertTrue(self._pf)

    def _raiseError(self, pf):
        with pf:
            raise ValueError('False alarm')

    def test_raiseException_expectPortFileCreated(self):
        self.assertRaises(ValueError, self._raiseError, self._pf)
        self.assertTrue(os.path.isfile(self._pf.path()))

    def test_raiseException_expectPortFileSize(self):
        self.assertRaises(ValueError, self._raiseError, self._pf)
        statDict = os.stat(self._pf.path())
        self.assertEqual(0, statDict[stat.ST_SIZE])

    def test_raiseException_expectPostState(self):
        self.assertRaises(ValueError, self._raiseError, self._pf)
        self.assertFalse(self._pf)

    def test_waitSequentially_expectReturnTrue(self):
        with self._pf:
            pass
        self.assertTrue(self._pf.wait())

    def test_waitSequentiallyWithException_expectReturnTrue(self):
        self.assertRaises(ValueError, self._raiseError, self._pf)
        self.assertTrue(self._pf.wait())

    def test_simulateTimeout_expectReturnTrue(self):
        mockTimer = mock.MagicMock(side_effect=[1, 60])
        with mock.patch('time.time', mockTimer):
            with self._pf:
                pass
            self.assertTrue(self._pf.wait())


if __name__ == '__main__':
    unittest.main()
