
import unittest

from accTest.objectModel import property


class TestProperty(unittest.TestCase):

    def test_name(self):
        self.assertEqual('hyref', property.Property('hyref', value='hyref://').name())

    def test_value(self):
        self.assertEqual('hyref://', property.Property('hyref', value='hyref://').value())
