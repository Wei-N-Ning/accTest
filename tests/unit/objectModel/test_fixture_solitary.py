
import unittest

from accTest.objectModel import fixture
from accTest.objectModel import baseTask


class TestFixture(unittest.TestCase):

    def setUp(self):
        self.f = fixture.Fixture()

    def test_expectDefaultState(self):
        self.assertFalse(self.f.hasProperty(''))
        self.assertFalse(self.f.getValue(''))
        self.assertFalse(self.f.getTasks())

    def test_setProperty_expectPropertyExists(self):
        self.f.setValue('foo', 1)
        self.assertTrue(self.f.hasProperty('foo'))

    def test_setProperty_expectValue(self):
        self.f.setValue('foo', 1)
        self.assertEqual(1, self.f.getValue('foo'))

    def test_setProperty_expectValueOverridden(self):
        self.f.setValue('foo', 1)
        self.f.setValue('foo', 12)
        self.assertEqual(12, self.f.getValue('foo'))

    def test_addTask_expectTaskExist(self):
        t = baseTask.BaseTask()
        self.f.addTask(t)
        self.assertEqual(t, self.f.iterTasks().next())

    def test_addTask_expectOrderOfTasks(self):
        fooTask = baseTask.BaseTask(instanceName='foo')
        barTask = baseTask.BaseTask(instanceName='bar')
        self.f.addTask(barTask)
        self.f.addTask(fooTask)
        self.assertEqual([barTask, fooTask], list(self.f.iterTasks()))

    def test_addTask_expectTaskOverridden(self):
        fooTask1 = baseTask.BaseTask(instanceName='foo')
        fooTask2 = baseTask.BaseTask(instanceName='foo')
        self.f.addTask(fooTask1)
        self.f.addTask(fooTask2)
        self.assertEqual([fooTask2], list(self.f.iterTasks()))
