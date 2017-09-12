import unittest

import mock
from accTest.execution.IOUtilities import ozEnv


createCmd = ozEnv.OzCmdLine.createFromEnviron


class TestOzCmdLine(unittest.TestCase):

    def test_expectNonEmptyCmdLine(self):
        self.assertTrue(ozEnv.OzCmdLine(ozArea='/').toStr())

    def test_expectDefaultOzExe(self):
        cmd_ = ozEnv.OzCmdLine(ozArea='/')
        self.assertEqual('/digi/var/oz/current/bin/bash_oz', cmd_.ozExe)
        self.assertTrue(cmd_.toStr().startswith('/digi/var/oz/current/bin/bash_oz'))

    def test_expectCustomOzExe(self):
        with mock.patch('os.path.isfile', mock.MagicMock(return_value=True)):
            cmd_ = ozEnv.OzCmdLine(ozExe='foobar', ozArea='/')
            self.assertTrue(cmd_.toStr().startswith('foobar'))

    def test_expectDefaultOzArea(self):
        cmd_ = ozEnv.OzCmdLine()
        self.assertEqual('/', cmd_.ozArea)
        self.assertTrue(cmd_.toStr().endswith('/'))

    def test_expectSpecificOzArea(self):
        areaPath = '/doom/e1m1'
        cmd_ = ozEnv.OzCmdLine(ozArea=areaPath)
        self.assertEqual(areaPath, cmd_.ozArea)
        self.assertTrue(cmd_.toStr().endswith(areaPath))

    def test_expectUsingArg(self):
        using = '/doom/e1m1'
        cmd_ = ozEnv.OzCmdLine(using=using)
        self.assertEqual(using, cmd_.using)
        self.assertTrue(cmd_.toStr().endswith('--using {}'.format(using)))

    def test_expectPaksToAdd(self):
        paks = ['imp-1.2.3', 'lostSoul-2.3.1']
        cmd_ = ozEnv.OzCmdLine(paksToAdd=paks)
        self.assertSequenceEqual(paks, cmd_.paksToAdd)
        self.assertTrue(cmd_.toStr().endswith('--add imp-1.2.3 --add lostSoul-2.3.1'))

    def test_expectFullCommandLine(self):
        with mock.patch('os.path.isfile', mock.MagicMock(return_value=True)):
            cmd_ = ozEnv.OzCmdLine(ozExe='doom', ozArea='/doom/e1m1', using='/e3m4',
                                   paksToAdd=['imp-1.2.3', 'lostSoul-2.3.1'])
            self.assertEqual('doom /doom/e1m1 --using /e3m4 --add imp-1.2.3 --add lostSoul-2.3.1', cmd_.toStr())

    def test_createFromEmptyEnvironDict_expectCommandLine(self):
        with mock.patch('os.path.isfile', mock.MagicMock(return_value=True)):
            cmd_ = createCmd(ozExe='doom')
            self.assertEqual('doom /', cmd_.toStr())

    def test_createFromPartialEnvironDict_expectCommandLine(self):
        with mock.patch('os.path.isfile', mock.MagicMock(return_value=True)):
            self.assertEqual('doom /e1m1', createCmd(ozExe='doom', environ={'OZ_CONTEXT': '/e1m1'}).toStr())
            self.assertEqual('doom /', createCmd(ozExe='doom', environ={'OZ_USING': '/e1m1'}).toStr())
            self.assertEqual('doom /e3m3/map --using /e1m1',
                             createCmd(ozExe='doom', environ={'OZ_CONTEXT': '/e3m3/map', 'OZ_USING': '/e1m1'}).toStr())
            self.assertEqual('doom / --add chainsaw-0.3.0 --add railgun-1.0.0',
                             createCmd(ozExe='doom', environ={'OZ_PAK_ADD': 'railgun-1.0.0:chainsaw-0.3.0'}).toStr())

    def test_createFromFullEnvironDict_expectCommandLine(self):
        with mock.patch('os.path.isfile', mock.MagicMock(return_value=True)):
            self.assertEqual('doom /e1m1 --using /e3m3/map --add chaingun-3.0.1 --add shotgun-0.9.3',
                             createCmd(ozExe='doom', environ={'OZ_CONTEXT': '/e1m1',
                                                              'OZ_USING': '/e3m3/map',
                                                              'OZ_PAK_ADD': 'shotgun-0.9.3:chaingun-3.0.1'}).toStr())


class StubFixture(object):

    def __init__(self, **kwargs):
        self._values = kwargs

    def getValue(self, k):
        return self._values.get(k)


class TestOzEnv(unittest.TestCase):

    def test_expectEnvEqual(self):
        env1 = ozEnv.OzEnv
        env1.cmd = ozEnv.OzCmdLine(ozExe='doom', ozArea='/doom/e1m1', using='/e3m4',
                                   paksToAdd=['imp-1.2.3', 'lostSoul-2.3.1'])
        env2 = ozEnv.OzEnv()
        env2.cmd = ozEnv.OzCmdLine(ozExe='doom', ozArea='/doom/e1m1', using='/e3m4',
                                   paksToAdd=['imp-1.2.3', 'lostSoul-2.3.1'])
        self.assertEqual(env1, env2)
        self.assertTrue(env1 in [env2])

    def test_expectEnvNotEqual(self):
        env1 = ozEnv.OzEnv
        env1.cmd = ozEnv.OzCmdLine(ozExe='doom', ozArea='/doom/e1m1', using='/e3m4',
                                   paksToAdd=['imp-1.2.3', 'lostSoul-2.3.1'])
        env2 = ozEnv.OzEnv()
        env2.cmd = ozEnv.OzCmdLine(ozExe='doom', ozArea='/doom/e1m1', using='/e2m4',
                                   paksToAdd=['imp-1.2.3'])
        self.assertNotEqual(env1, env2)

    def test_expectHashing(self):
        env1 = ozEnv.OzEnv()
        env1.cmd = ozEnv.OzCmdLine(ozExe='doom', ozArea='/doom/e1m1', using='/e3m4',
                                   paksToAdd=['imp-1.2.3', 'lostSoul-2.3.1'])
        env2 = ozEnv.OzEnv()
        env2.cmd = ozEnv.OzCmdLine(ozExe='doom', ozArea='/doom/e1m1', using='/e3m4',
                                   paksToAdd=['imp-1.2.3', 'lostSoul-2.3.1'])
        self.assertEqual(hash(env1), hash(env2))

    def test_createFromFixture_expectCreatedFromArguments(self):
        with mock.patch('os.path.isfile', mock.MagicMock(return_value=True)):
            f = StubFixture(ozExe='doom')
            env1 = ozEnv.OzEnv.fromFixture(f)
            self.assertTrue(env1.cmd.toStr().startswith('doom / --add'))

    def test_createFromFixture_expectCreatedFromEnviron(self):
        with mock.patch('os.path.isfile', mock.MagicMock(return_value=True)):
            f = StubFixture(ozExe='doom', useCurrentEnvironment=True)
            env1 = ozEnv.OzEnv.fromFixture(f)
            self.assertTrue(env1.cmd.toStr())


if __name__ == '__main__':
    unittest.main()
