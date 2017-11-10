"""Testing utilities"""
# pylint: disable=too-many-public-methods
import sqlite3
import unittest


class DBTestCase(unittest.TestCase):
    """SQLite DB testing"""

    test_db = ':memory:'

    def setUp(self):
        self.db_conn = sqlite3.connect(self.test_db)
        self.db_cur = self.db_conn.cursor()

    def tearDown(self):
        self.db_conn.close()
