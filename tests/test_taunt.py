"""Tests the taunt module"""
# pylint: disable=redefined-outer-name
import pytest

from botibal.models import Taunt
from botibal.taunt import DEFAULT_AGGRO, Tauntionary


@pytest.fixture
def tauntionary(testdb):
    """Tauntionary"""
    _, session = testdb
    return Tauntionary(session)


def taunts2list(taunts):
    """Return taunts as a list of tuples"""
    return [(taunt.id, taunt.nick, taunt.text, taunt.aggro) for taunt in taunts]


def test_init_empty_db(testdb):
    """Check a DB is created with an empty 'taunt' table"""
    _, session = testdb
    tauntionary = Tauntionary(session)
    assert tauntionary.taunts.all() == []
    assert tauntionary.taunts.count() == 0


def test_init_db(testdb):
    """Load an existing DB"""
    _, session = testdb
    tauntionary = Tauntionary(session)
    taunt = Taunt(nick="h4xx0r", text="rtfm, n00b!", aggro=3)
    session.add(taunt)
    session.commit()
    tauntionary = Tauntionary(session)
    assert taunts2list(tauntionary.taunts.all()) == \
        [(1, u'h4xx0r', u'rtfm, n00b!', 3)]


def test_add_taunt(tauntionary):
    """Add new entries to the DB"""
    tauntionary.add_taunt("imah firin' mah laser!", "whoop")
    assert taunts2list(tauntionary.taunts.all()) == \
        [(1, u'whoop', u"imah firin' mah laser!", DEFAULT_AGGRO)]

    tauntionary.add_taunt("you say what what?", "butters", 3)
    assert taunts2list(tauntionary.taunts.all()) == \
        [
            (1, u'whoop', u"imah firin' mah laser!", DEFAULT_AGGRO),
            (2, u'butters', u'you say what what?', 3)
        ]


def test_add_accented_taunt(tauntionary):
    """Add a taunt containing accented chars"""
    tauntionary.add_taunt('åéàè', 'ïùø')
    assert taunts2list(tauntionary.taunts.all()) == \
        [(1, u'\xef\xf9\xf8', u'\xe5\xe9\xe0\xe8', DEFAULT_AGGRO)]


def test_add_unicode_taunt(tauntionary):
    """Add a taunt containing accented chars (unicode)"""
    tauntionary.add_taunt(u'åéàè', u'ïùø')
    assert taunts2list(tauntionary.taunts.all()) == \
        [(1, u'\xef\xf9\xf8', u'\xe5\xe9\xe0\xe8', DEFAULT_AGGRO)]


def test_add_empty_taunt(tauntionary):
    """Attempt to add an empty taunt"""
    with pytest.raises(ValueError):
        tauntionary.add_taunt(None, 'void')
    with pytest.raises(ValueError):
        tauntionary.add_taunt('', 'void')


def test_add_taunt_with_empty_nick(tauntionary):
    """Attempt to add a taunt for a void user"""
    with pytest.raises(ValueError):
        tauntionary.add_taunt('shoop', None)
    with pytest.raises(ValueError):
        tauntionary.add_taunt('whoop', '')


def test_add_duplicate_taunt(tauntionary):
    """Attempt to add the same taunt twice"""
    tauntionary.add_taunt("imah firin' mah laser!", "whoop")
    with pytest.raises(ValueError):
        tauntionary.add_taunt("imah firin' mah laser!", "whoop")


def test_empty_taunt_list(tauntionary):
    """Ensure an error is raised if the list is empty"""
    with pytest.raises(ValueError):
        tauntionary.taunt()


def test_list_by_aggro(tauntionary):
    """List.taunts.all() by aggro level"""
    tauntionary.add_taunt("imah firin' mah laser!", "whoop", 5)
    tauntionary.add_taunt("trololo!", "khail", 3)
    tauntionary.add_taunt("you say what what?", "butters", 3)
    assert tauntionary.list_by_aggro() == \
        (
            'lv.3\n------\n'
            '  2 - trololo!\n'
            '  3 - you say what what?\n'
            'lv.5\n------\n'
            "  1 - imah firin' mah laser!\n"
        )


def test_repr(tauntionary):
    """Display the Tauntionary as a string"""
    tauntionary.add_taunt("imah firin' mah laser!", "whoop")
    assert str(tauntionary) == \
        "1 - imah firin' mah laser! (lv.{}, whoop)".format(DEFAULT_AGGRO)

    tauntionary.add_taunt("you say what what?", "butters", 3)
    assert str(tauntionary) == \
        (
            "1 - imah firin' mah laser! (lv.{}, whoop)\n"
            "2 - you say what what? (lv.3, butters)"
            .format(DEFAULT_AGGRO)
        )


def test_set_aggro(tauntionary):
    """Change the aggressivity level of a taunt"""
    tauntionary.add_taunt("imah firin' mah laser!", "whoop", 1)
    assert str(tauntionary) == "1 - imah firin' mah laser! (lv.1, whoop)"

    tauntionary.set_aggro(1, 3)
    assert str(tauntionary) == "1 - imah firin' mah laser! (lv.3, whoop)"


def test_set_negative_aggro(tauntionary):
    """Change the aggressivity level of a taunt"""
    tauntionary.add_taunt("imah firin' mah laser!", "whoop", 1)
    assert str(tauntionary) == "1 - imah firin' mah laser! (lv.1, whoop)"

    tauntionary.set_aggro(1, -3)
    assert str(tauntionary) == "1 - imah firin' mah laser! (lv.3, whoop)"
