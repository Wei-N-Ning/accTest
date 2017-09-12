
import unittest

from accTest.objectModel import baseTask
from accTest import exceptions

import mock


class TestBaseTask(unittest.TestCase):

    def test_orphanTask_expectRaisesWhenGetValue(self):
        t = baseTask.BaseTask()
        self.assertRaises(exceptions.BrokenTask, t.getValue, '')

    def test_orphanTask_expectRaisesWhenRun(self):
        t = baseTask.BaseTask()
        self.assertRaises(exceptions.BrokenTask, t.run)

    def test_expectFullName(self):
        t = baseTask.BaseTask()
        self.assertEqual('BaseTask', t.fullName())
        t = baseTask.BaseTask(instanceName='DoThis')
        self.assertEqual('BaseTask:DoThis', t.fullName())

    def test_expectInstanceName(self):
        t = baseTask.BaseTask()
        self.assertFalse(t.instanceName())
        t = baseTask.BaseTask(instanceName='DoThis')
        self.assertEqual('DoThis', t.instanceName())

    def test_expectName(self):
        self.assertTrue('BaseTask' == baseTask.BaseTask().name() == baseTask.BaseTask('DoThis').name())

    def test_hasFixture_expectGetValue(self):
        t = baseTask.BaseTask()
        f = mock.MagicMock()
        f.getValue.return_value = '12 gauge'
        t.attachToFixture(f)
        self.assertEqual('12 gauge', t.getValue('caliber'))

    def test_hasFixture_expectGetFixture(self):
        t = baseTask.BaseTask()
        self.assertFalse(t.getFixture())
        f = mock.MagicMock()
        t.attachToFixture(f)
        self.assertEqual(f, t.getFixture())

    def test_expectArguments(self):
        t = baseTask.BaseTask()
        self.assertFalse(t.arguments())
        t = baseTask.BaseTask(1, 2)
        self.assertEqual((1, 2), t.arguments())

    def test_run_expectFail(self):
        t = baseTask.BaseTask()
        f = mock.MagicMock()
        t.attachToFixture(f)
        self.assertFalse(t.run())
