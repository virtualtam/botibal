# -*- coding: utf-8 -*-
"""
I swear...
"""
import random

DEFAULT_AGGRO = 4


class Tauntionary(object):
    """
    A nice collection of charming sentences
    """

    def __init__(self, database_connection):
        self.taunts = []
        self.db_conn = database_connection
        self.db_cur = self.db_conn.cursor()
        self.init_db()

    def __repr__(self):
        return '\n'.join(
            ['{} - {} (lv.{}, {})'.format(t_id, t_text, t_aggro, t_nick)
             for t_id, t_nick, t_text, t_aggro in self.taunts])

    def init_db(self):
        """
        Initializes DB interaction

        Actions:
        - create table if necessary,
        - load data.
        """
        self.db_cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS taunt (
            id    INTEGER PRIMARY KEY,
            nick  TEXT,
            text  TEXT,
            aggro INTEGER DEFAULT 5)
            ''')
        self.db_conn.commit()
        self.load_from_db()

    def load_from_db(self):
        """
        Loads taunts from the database
        """
        self.taunts = self.db_cur.execute('SELECT * FROM taunt').fetchall()

    def list_by_aggro(self):
        """
        Lists all taunts, sorted by aggro level
        """
        taunts = self.db_cur.execute('SELECT id, text, aggro FROM taunt '
                                     'ORDER BY aggro, id').fetchall()

        t_list = ''
        current_aggro = ''

        for t_id, t_text, t_aggro in taunts:
            if t_aggro != current_aggro:
                t_list += 'lv.{}\n------\n'.format(t_aggro)
                current_aggro = t_aggro

            t_list += '  {} - {}\n'.format(t_id, t_text)

        return t_list

    def add_taunt(self, taunt, nick, aggro=DEFAULT_AGGRO):
        """
        Adds a new taunt
        """
        if taunt is None or taunt == '':
            raise ValueError('Empty taunt')

        if nick is None or nick == '':
            raise ValueError('Taunt: empty user nickname')

        if taunt in [text for _, _, text, _ in self.taunts]:
            raise ValueError('This taunt already exists!')

        self.db_cur.execute(
            'INSERT INTO taunt VALUES(NULL,?,?,?)',
            (nick, taunt, aggro))
        self.db_conn.commit()
        self.load_from_db()

    def set_aggro(self, t_id, aggro):
        """
        Changes the aggressivity level of a taunt
        """
        self.db_cur.execute('UPDATE taunt SET aggro=? WHERE id=?',
                            (abs(int(aggro)), int(t_id)))
        self.db_conn.commit()
        self.load_from_db()

    def taunt(self, t_id=None):
        """
        You piece of...
        """
        if t_id is not None:
            return self.taunts[int(t_id) - 1][2]
        return self.taunts[random.randint(0, len(self.taunts) - 1)][2]
