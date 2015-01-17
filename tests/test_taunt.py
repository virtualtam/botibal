# -*- coding: utf-8 -*-
# pylint: disable=too-many-public-methods
'Tests the taunt module'
import unittest
from minibal.taunt import Tauntionary
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

    def test_empty_taunt(self):
        'Ensure an error is raised if the list is empty'
        with self.assertRaises(ValueError):
            self.tauntionary.taunt()

    def test_taunt(self):
        'Ensure Unicode strings are returned'
        self.tauntionary.add_taunt("imah firin' mah laser!", "whoop")
        self.tauntionary.add_taunt("you say what what?", "butters")
        self.assertEqual(type(self.tauntionary.taunt()), unicode)


if __name__ == '__main__':
    unittest.main()
