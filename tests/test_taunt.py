# -*- coding: utf-8 -*-
# pylint: disable=too-many-public-methods
'Tests the taunt module'
import unittest
from botibal.taunt import Tauntionary
from tests.utils import DBTestCase


class TestTauntionary(DBTestCase):
    'Be nice!'
    def setUp(self):
        super(TestTauntionary, self).setUp()
        self.tauntionary = Tauntionary(self.db_conn)

    def test_init_empty_db(self):
        'Check a DB is created with an empty "taunt" table'
        self.assertEqual(self.tauntionary.taunts, [])
        self.assertEqual(
            self.db_cur.execute('SELECT * FROM taunt').fetchall(), [])

    def test_init_db(self):
        'Load an existing DB'
        self.db_cur.execute(
            'INSERT INTO taunt VALUES(NULL,"h4xx0r","rtfm, n00b!")')
        self.db_conn.commit()
        self.tauntionary = Tauntionary(self.db_conn)
        self.assertEqual(self.tauntionary.taunts,
                         [(1, u'h4xx0r', u'rtfm, n00b!')])

    def test_add_taunt(self):
        'Add new entries to the DB'
        self.tauntionary.add_taunt("imah firin' mah laser!", "whoop")
        self.assertEqual(self.tauntionary.taunts,
                         [(1, u'whoop', u"imah firin' mah laser!")])
        self.tauntionary.add_taunt("you say what what?", "butters")
        self.assertEqual(self.tauntionary.taunts,
                         [(1, u'whoop', u"imah firin' mah laser!"),
                          (2, u'butters', u'you say what what?')])

    def test_add_accented_taunt(self):
        'Add a taunt containing accented chars'
        self.tauntionary.add_taunt('åéàè', 'ïùø')
        self.assertEqual(self.tauntionary.taunts,
                         [(1, u'\xef\xf9\xf8', u'\xe5\xe9\xe0\xe8')])

    def test_add_unicode_taunt(self):
        'Add a taunt containing accented chars (unicode)'
        self.tauntionary.add_taunt(u'åéàè', u'ïùø')
        self.assertEqual(self.tauntionary.taunts,
                         [(1, u'\xef\xf9\xf8', u'\xe5\xe9\xe0\xe8')])

    def test_add_empty_taunt(self):
        'attempt to add an empty taunt'
        with self.assertRaises(ValueError):
            self.tauntionary.add_taunt(None, 'void')
        with self.assertRaises(ValueError):
            self.tauntionary.add_taunt('', 'void')

    def test_add_taunt_with_empty_nick(self):
        'Attempt to add a taunt for a void user'
        with self.assertRaises(ValueError):
            self.tauntionary.add_taunt('shoop', None)
        with self.assertRaises(ValueError):
            self.tauntionary.add_taunt('whoop', '')

    def test_add_duplicate_taunt(self):
        'Attempt to add the same taunt twice'
        self.tauntionary.add_taunt("imah firin' mah laser!", "whoop")
        with self.assertRaises(ValueError):
            self.tauntionary.add_taunt("imah firin' mah laser!", "whoop")

    def test_empty_taunt_list(self):
        'Ensure an error is raised if the list is empty'
        with self.assertRaises(ValueError):
            self.tauntionary.taunt()

    def test_repr(self):
        'Display the Tauntionary as a string'
        self.tauntionary.add_taunt("imah firin' mah laser!", "whoop")
        self.assertEqual(str(self.tauntionary),
                         "1 - imah firin' mah laser! (whoop)")
        self.tauntionary.add_taunt("you say what what?", "butters")
        self.assertEqual(str(self.tauntionary),
                         "1 - imah firin' mah laser! (whoop)\n"
                         "2 - you say what what? (butters)")

    def test_taunt(self):
        'Ensure Unicode strings are returned'
        self.tauntionary.add_taunt("imah firin' mah laser!", "whoop")
        self.tauntionary.add_taunt("you say what what?", "butters")
        self.assertEqual(type(self.tauntionary.taunt()), unicode)

    def test_taunt_id(self):
        'Pick a taunt with its ID'
        self.tauntionary.add_taunt("imah firin' mah laser!", "whoop")
        self.tauntionary.add_taunt("you say what what?", "butters")
        self.assertEqual(type(self.tauntionary.taunt(2)), unicode)
        self.assertEqual(type(self.tauntionary.taunt('2')), unicode)


if __name__ == '__main__':
    unittest.main()
