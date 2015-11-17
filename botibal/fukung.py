# -*- coding: utf-8 -*-
"""
Fukung interaction
"""
import random
import re

BASE_URL = 'http://www.fukung.net/v/'
REGEX = r'http://(www\.)?fukung.net/v/(\d+)/(\w+)\.(\w+)'


class Fukung(object):
    """
    Manages fukung.net links
    """

    def __init__(self, database_connection):
        self.link_ids = []
        self.db_conn = database_connection
        self.db_cur = self.db_conn.cursor()
        self.init_db()

    def __repr__(self):
        return '\n'.join(
            ['{} - {}{}'.format(f_id, BASE_URL, f_link)
             for f_id, f_link in self.link_ids]
        )

    def init_db(self):
        """
        Initializes DB interaction

        Actions:
        - create table if necessary,
        - load data.
        """
        self.db_cur.execute(
            '''CREATE TABLE IF NOT EXISTS fukung (
            id INTEGER PRIMARY KEY,
            link_id TEXT)''')
        self.db_conn.commit()
        self.load_from_db()

    def load_from_db(self):
        """
        Loads links from the database
        """
        self.link_ids = self.db_cur.execute('SELECT * FROM fukung').fetchall()

    def add_link_url(self, text):
        """
        Adds a new link url
        """
        matches = re.search(REGEX, text)

        if not matches:
            return

        link_id = '{}/{}.{}'.format(
            matches.group(2),
            matches.group(3),
            matches.group(4)
        )
        self.add_link_id(link_id)

    def add_link_id(self, link_id):
        """
        Adds a new link id
        """
        if link_id in [lid for _, lid in self.link_ids]:
            raise ValueError('Duplicate Fukung link')

        self.db_cur.execute('INSERT INTO fukung VALUES(NULL,?)', (link_id,))
        self.db_conn.commit()
        self.load_from_db()

    def get_link(self):
        """
        Well, well, well, what do we have here?
        """
        return '{}{}'.format(
            BASE_URL,
            self.link_ids[random.randint(0, len(self.link_ids) - 1)][1]
        )
