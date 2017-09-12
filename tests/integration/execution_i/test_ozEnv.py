import unittest

from accTest import DSL
from accTest import resources
from accTest.execution.IOUtilities import ozEnv


class TestFixtureIndexesByEnv(unittest.TestCase):

    def setUp(self):
        self.dslFilePath = resources.filePath('dslExample.py')
        self.fixtures = DSL.parse(self.dslFilePath, instantiation=False)

    def test_expectNumOfFixtureGroups(self):
        fDict = ozEnv.fixtureIndexesByEnv(self.fixtures)
        self.assertEqual(2, len(fDict))

    def test_expectOzAreas(self):
        fDict = ozEnv.fixtureIndexesByEnv(self.fixtures)
        env1 = fDict.keys()[0]
        env2 = fDict.keys()[1]
        self.assertEqual(
            {'/weta/shots/test/GEN', '/weta/dev/GEN/base'},
            {env1.cmd.ozArea, env2.cmd.ozArea})


if __name__ == '__main__':
    unittest.main()
