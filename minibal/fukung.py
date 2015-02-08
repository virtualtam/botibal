# -*- coding: utf-8 -*-
'Fukung interaction'
import random


BASE_URL = 'http://www.fukung.net/v/'
REGEX = r'http://(www\.)?fukung.net/v/(\d+)/(\w+)\.(\w+)'


class Fukung(object):
    'Manages fukung.net links'
    def __init__(self, database_connection):
        self.link_ids = []
        self.db_conn = database_connection
        self.db_cur = self.db_conn.cursor()
        self.init_db()

    def __repr__(self):
        return '\n'.join(['{} - {}{}'.format(f_id, BASE_URL, f_link)
                          for f_id, f_link in self.link_ids])

    def init_db(self):
        """
        Initializes DB interaction:
        - creates table if necessary,
        - loads data.
        """
        self.db_cur.execute(
            '''CREATE TABLE IF NOT EXISTS fukung (
            id INTEGER PRIMARY KEY,
            link_id TEXT)''')
        self.db_conn.commit()
        self.load_from_db()

    def load_from_db(self):
        'Loads links from the database'
        self.link_ids = self.db_cur.execute('SELECT * FROM fukung').fetchall()

    def add_link_url(self, matchobject):
        'Adds a new link url'
        # TODO: move regex matching from botibal to there (error handling)
        link_id = '{}/{}.{}'.format(matchobject.group(2),
                                    matchobject.group(3),
                                    matchobject.group(4))
        self.add_link_id(link_id)

    def add_link_id(self, link_id):
        'Adds a new link id'
        # TODO: check duplicates
        self.db_cur.execute('INSERT INTO fukung VALUES(NULL,?)', (link_id,))
        self.db_conn.commit()
        self.load_from_db()

    def get_link(self):
        'Well, well, well, what do we have here?'
        return '{}{}'.format(
            BASE_URL,
            self.link_ids[random.randint(0, len(self.link_ids) - 1)][1])
