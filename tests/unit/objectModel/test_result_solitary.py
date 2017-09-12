
import unittest

from accTest.objectModel import result


class TestResult(unittest.TestCase):

    def test_expectEvaluation(self):
        self.assertFalse(result.Result('', False))
        self.assertTrue(result.Result('', True))

    def test_expectName(self):
        self.assertFalse(result.Result('', False).name())
        self.assertEqual('Monkey', result.Result('Monkey', False).name())

    def test_expectStringFormat(self):
        self.assertEqual('Monkey:False', str(result.Result('Monkey', False)))
