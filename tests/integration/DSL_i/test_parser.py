
import unittest

from accTest import exceptions
from accTest import resources
from accTest.DSL import parser


class TestParser(unittest.TestCase):

    def setUp(self):
        self.dslFilePath = resources.filePath('dslExample.py')
        self.p = parser.Parser()

    def test_invalidDslFilePath_expectRaises(self):
        self.assertRaises(exceptions.InvalidDslFilePath, self.p.parse, '')
        self.assertRaises(exceptions.InvalidDslFilePath, self.p.parse, '/non/existing/file')

    def test_validDslFilePath_expectFixturesCreated(self):
        fixtures = self.p.parse(self.dslFilePath)
        self.assertTrue(fixtures)

    def test_expectNumFixtures(self):
        fixtures = self.p.parse(self.dslFilePath)
        self.assertEqual(3, len(fixtures))

    def test_expectFixtureProperties(self):
        fixtures = self.p.parse(self.dslFilePath)
        f1 = fixtures[0]
        self.assertEqual('/hft/shots/fif/0110', f1.getValue('hydraGroup'))
        f3 = fixtures[2]
        self.assertEqual('fireball01', f3.getValue('productName'))

    def test_expectFixtureTasks(self):
        fixtures = self.p.parse(self.dslFilePath)
        f2 = fixtures[1]
        tasks = f2.getTasks()
        self.assertEqual(4, len(tasks))
        self.assertEqual('DemoImportElement', tasks['DemoImportElement'].fullName())
        self.assertEqual('DemoSharedTask', tasks['DemoSharedTask'].fullName())
        self.assertEqual('DemoExportElement', tasks['DemoExportElement'].fullName())
        self.assertEqual('DemoAssertKeyframesOnElement', tasks['DemoAssertKeyframesOnElement'].fullName())

    def test_expectInheritingGlobalProperties(self):
        fixtures = self.p.parse(self.dslFilePath)
        f1 = fixtures[0]
        self.assertEqual('foobar', f1.getValue('foobar'))
        f2 = fixtures[1]
        self.assertEqual('/weta/shots/test/GEN', f2.getValue('ozArea'))
        f3 = fixtures[2]
        self.assertEqual('/hft/shots/test/GEN', f3.getValue('hydraGroup'))

    def test_parseWhileFilteringByIndexes_expectResultingFixtures(self):
        fixtures = self.p.parse(self.dslFilePath, indexes=[1])
        self.assertEqual(1, len(fixtures))
        self.assertEqual('fireball01', fixtures[0].getValue('productName'))
