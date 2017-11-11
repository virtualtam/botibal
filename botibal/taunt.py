"""I swear..."""
import random

from sqlalchemy import text

from botibal.models import Taunt

DEFAULT_AGGRO = 4


class Tauntionary(object):
    """A nice collection of charming sentences"""

    def __init__(self, session):
        self.session = session

    def __repr__(self):
        return "\n".join([
            "{} - {} (lv.{}, {})".format(t.id, t.text, t.aggro, t.nick)
            for t in self.taunts.all()
        ])

    @property
    def taunts(self):
        """Load taunts from the database"""
        return self.session.query(Taunt)

    def list_by_aggro(self):
        """Lists all taunts, sorted by aggro level"""
        taunts = self.taunts.from_statement(
            text('SELECT id, text, aggro FROM taunt ORDER BY aggro, id')
        ).all()

        t_list = ''
        current_aggro = ''

        for taunt in taunts:
            if taunt.aggro != current_aggro:
                t_list += 'lv.{}\n------\n'.format(taunt.aggro)
                current_aggro = taunt.aggro

            t_list += '  {} - {}\n'.format(taunt.id, taunt.text)

        return t_list

    def add_taunt(self, taunt_text, nick, aggro=DEFAULT_AGGRO):
        """Adds a new taunt"""
        if not taunt_text:
            raise ValueError('Empty taunt')

        if not nick:
            raise ValueError('Taunt: empty user nickname')

        if taunt_text in [taunt.text for taunt in self.taunts.all()]:
            raise ValueError('This taunt already exists!')

        taunt = Taunt(nick=nick, text=taunt_text, aggro=aggro)
        self.session.add(taunt)
        self.session.commit()

    def set_aggro(self, t_id, aggro):
        """Changes the aggressivity level of a taunt"""
        taunt = self.taunts.get(int(t_id))
        taunt.aggro = abs(int(aggro))
        self.session.commit()

    def taunt(self, t_id=None):
        """You piece of..."""
        count = self.taunts.count()
        if not t_id:
            t_id = random.randint(1, count)
        taunt = self.taunts.get(int(t_id))
        return taunt.text
