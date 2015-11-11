# -*- coding: utf-8 -*-
# pylint: disable=too-many-public-methods
"""
Testing utilities
"""
import os
import sqlite3
import unittest


class DBTestCase(unittest.TestCase):
    """
    SQLite DB testing
    """

    test_db = os.path.join('tests', 'test.db')

    def setUp(self):
        if os.path.lexists(self.test_db):
            os.remove(self.test_db)

        self.db_conn = sqlite3.connect(self.test_db)
        self.db_cur = self.db_conn.cursor()

    def tearDown(self):
        self.db_conn.close()
