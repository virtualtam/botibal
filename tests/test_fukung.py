# -*- coding: utf-8 -*-
# pylint: disable=too-many-public-methods
"""
Tests the fukung module
"""
import re
import unittest

from botibal.fukung import BASE_URL, REGEX, Fukung
from tests.utils import DBTestCase


class TestFukung(DBTestCase):
    """
    Kung-Fu!
    """

    def setUp(self):
        super(TestFukung, self).setUp()
        self.fukung = Fukung(self.db_conn)

    def test_init_empty_db(self):
        """
        Check a DB is created with an empty 'fukung' table
        """
        self.assertEqual(self.fukung.link_ids, [])
        self.assertEqual(
            self.db_cur.execute('SELECT * FROM fukung').fetchall(), [])

    def test_init_db(self):
        """
        Load an existing DB
        """
        self.db_cur.execute(
            'INSERT INTO fukung VALUES(NULL,"0/test0.gif")')
        self.db_conn.commit()
        self.fukung = Fukung(self.db_conn)
        self.assertEqual(self.fukung.link_ids,
                         [(1, u'0/test0.gif')])

    def test_add_link_id(self):
        """
        Add new entries to the DB
        """
        self.fukung.add_link_id('1/test1.jpg')
        self.assertEqual(self.fukung.link_ids,
                         [(1, u'1/test1.jpg')])
        self.fukung.add_link_id('2/test2.png')
        self.assertEqual(self.fukung.link_ids,
                         [(1, u'1/test1.jpg'),
                          (2, u'2/test2.png')])

    def test_add_duplicate_link_id(self):
        """
        Attempt to add the same link twice
        """
        self.fukung.add_link_id('1/test1.jpg')
        with self.assertRaises(ValueError):
            self.fukung.add_link_id('1/test1.jpg')

    def test_empty_link(self):
        """
        Ensure an error is raised if the list is empty
        """
        with self.assertRaises(ValueError):
            self.fukung.get_link()

    def test_add_link_url(self):
        """
        Add a valid fukung link
        """
        url = BASE_URL + '4/v4l1d.gif'
        self.fukung.add_link_url(url)
        self.assertEqual(self.fukung.link_ids,
                         [(1, u'4/v4l1d.gif')])

    def test_add_bad_link_url(self):
        """
        Add a valid fukung link
        """
        url = BASE_URL + '/5/1nv4l1d'
        self.fukung.add_link_url(url)
        self.assertEqual(self.fukung.link_ids, [])

    def test_repr(self):
        """
        Display the list as a string
        """
        self.fukung.add_link_id('1/test1.jpg')
        self.assertEqual(str(self.fukung),
                         '1 - http://www.fukung.net/v/1/test1.jpg')
        self.fukung.add_link_id('2/test2.png')
        self.assertEqual(str(self.fukung),
                         '1 - http://www.fukung.net/v/1/test1.jpg\n'
                         '2 - http://www.fukung.net/v/2/test2.png')

    def test_get_link(self):
        """
        Ensure valid links are returned
        """
        self.fukung.add_link_id('1/test1.jpg')
        self.fukung.add_link_id('2/test2.png')
        link = self.fukung.get_link()
        self.assertEqual(type(link), str)
        self.assertTrue(re.match(REGEX, link))


if __name__ == '__main__':
    unittest.main()
