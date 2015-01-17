# -*- coding: utf-8 -*-
'I swear...'
import random


class Tauntionary(object):
    'A nice collection of charming sentences'
    def __init__(self, database_connection):
        self.taunts = []
        self.db_conn = database_connection
        self.db_cur = self.db_conn.cursor()
        self.init_db()

    def __repr__(self):
        # pylint: disable=star-args
        return '\n'.join(['{} - {} ({})'.format(*taunt)
                          for taunt in self.taunts])

    def init_db(self):
        """
        Initializes DB interaction:
        - creates table if necessary,
        - loads data.
        """
        self.db_cur.execute(
            '''CREATE TABLE  IF NOT EXISTS taunt (
            id INTEGER PRIMARY KEY,
            nick TEXT,
            text TEXT)''')
        self.db_conn.commit()
        self.load_from_db()

    def load_from_db(self):
        'Loads taunts from the database'
        self.taunts = self.db_cur.execute('SELECT * FROM taunt').fetchall()

    def add_taunt(self, taunt, nick):
        'Adds a new taunt'
        self.db_cur.execute('INSERT INTO taunt VALUES(NULL,?,?)', (nick, taunt))
        self.db_conn.commit()
        self.load_from_db()

    def taunt(self):
        'You piece of...'
        return self.taunts[random.randint(0, len(self.taunts) - 1)][2]
