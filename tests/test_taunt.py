# -*- coding: utf-8 -*-
# pylint: disable=too-many-public-methods
'Tests the taunt module'
import os
import shutil
import unittest
from taunt import Tauntionary

TEST_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_REF = os.path.join(TEST_DIR, 'taunts')
TEST_FILE = os.path.join(TEST_DIR, 'tmp_taunts')


class TestTauntionary(unittest.TestCase):
    'Be nice!'

    def setUp(self):
        shutil.copyfile(TEST_REF, TEST_FILE)
        self.tauntionary = Tauntionary(TEST_FILE)

    @classmethod
    def tearDownClass(cls):
        if os.path.isfile(TEST_FILE):
            os.remove(TEST_FILE)

    def test_load_from_file(self):
        'Load taunts from a text file'
        self.assertEqual(len(self.tauntionary.taunts), 3)

    def test_add_and_save_taunt(self):
        'Add a new taunt and save the file'
        self.tauntionary.add_taunt('Python, do you speak it, mofo?')
        self.assertEqual(len(self.tauntionary.taunts), 4)

        self.tauntionary = Tauntionary(TEST_FILE)
        self.assertEqual(len(self.tauntionary.taunts), 4)


if __name__ == '__main__':
    unittest.main()
