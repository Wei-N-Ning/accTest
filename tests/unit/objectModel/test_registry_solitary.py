
import unittest

from accTest.objectModel import registry


class TestRegistry(unittest.TestCase):

    def setUp(self):
        registry.clear()

    def tearDown(self):
        registry.clear()

    def test_expectClassRegistered(self):
        class Monkey(object):
            __metaclass__ = registry.Registry
        self.assertEqual(Monkey, registry.get('Monkey'))

    def test_clear_expectClassNotRegistered(self):
        class Monkey(object):
            __metaclass__ = registry.Registry
        registry.clear()
        self.assertFalse(registry.get('Monkey'))
