
import unittest

from accTest import exceptions
from accTest import resources
from accTest.DSL import factory


class TestFindAndImport(unittest.TestCase):

    def setUp(self):
        self.dslFilePath = resources.filePath('dslExample.py')

    def test_expectTaskFile(self):
        taskFilePath = factory.findTaskFile(self.dslFilePath, 'Foo')
        self.assertEqual(resources.filePath('dslExample/Foo.py'), taskFilePath)

    def test_expectTaskFileNotFind(self):
        self.assertFalse(factory.findTaskFile(self.dslFilePath, 'Foooo'))

    def test_expectModuleObj(self):
        taskFilePath = factory.findTaskFile(self.dslFilePath, 'Foo')
        mod = factory.importPythonModule(taskFilePath)
        self.assertTrue(mod)


class TestFactory(unittest.TestCase):

    def setUp(self):
        self.dslFilePath = resources.filePath('dslExample.py')
        self.f = factory.TaskFactory(self.dslFilePath)

    def test_invalidTaskName_expectNoTaskCreated(self):
        self.assertFalse(self.f.create('....'))

    def test_failToImport_expectRaises(self):
        self.assertRaises(exceptions.CanNotLoadTask, self.f.create, 'DemoTaskThatRaises')

    def test_invalidTaskName_expectRaises(self):
        self.assertRaises(exceptions.MalformedTaskName, self.f.create, 'asdsad:sad:asd')

    def test_missingTaskClass_expectTaskCreated(self):
        self.assertFalse(self.f.create('DemoMissingClass'))

    def test_expectTaskFromDslDirectoryCreated(self):
        task = self.f.create('DemoAssertElementExists')
        self.assertTrue(task)
        self.assertEqual('DemoAssertElementExists', task.fullName())

    def test_expectTaskFromDslDirectory_useInstanceName(self):
        self.assertEqual('DemoAssertElementExists:Instance1',
                         self.f.create('DemoAssertElementExists:Instance1').fullName())

    def test_expectTaskFromSharedModuleCreated(self):
        task = self.f.create('DemoSharedTask')
        self.assertTrue(task)
        self.assertEqual('DemoSharedTask', task.fullName())

    def test_expectTaskFromSharedModule_useInstanceName(self):
        self.assertEqual('DemoSharedTask:instance1',
                         self.f.create('DemoSharedTask:instance1').fullName())
