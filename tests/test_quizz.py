"""Tests the quizz module"""
# pylint: disable=redefined-outer-name
import pytest

from botibal.quizz import Quizz, ScoreDict


@pytest.fixture
def scores():
    """Quizz ScoreDict"""
    return ScoreDict()


def test_add_score(scores):
    """Add a new score"""
    scores.add_score('Luke', 1)
    assert scores['Luke'] == 1


def test_add_string_score(scores):
    """Add a new score: integer represented as a string"""
    scores.add_score('Luke', '10')
    assert scores['Luke'] == 10


def test_add_invalid_score(scores):
    """Attempt to add a string"""
    with pytest.raises(ValueError):
        scores.add_score('Luke', 'Use the Force')


def test_increment_score(scores):
    """Wow, that guy is good! Look, he scored, twice!"""
    scores.add_score('Luke', 1)
    assert scores['Luke'] == 1
    scores.add_score('Luke', 1)
    assert scores['Luke'] == 2


def test_reset(scores):
    """Re-settle the scores!"""
    scores.add_score('Luke', 7)
    scores.add_score('Vader', 5)
    scores.reset()
    assert scores['Luke'] == 0
    assert scores['Vader'] == 0


def test_results(scores):
    """Display the scores as a string"""
    scores.add_score('Luke', 1)
    assert scores.results() == 'Luke: 1'

    scores.add_score('Luke', 3)
    scores.add_score('Vader', 333)
    assert scores.results() == 'Luke: 4\nVader: 333'

    scores.add_score('Vader', 333)
    assert scores.results() == 'Luke: 4\nVader: 666'


@pytest.fixture
def quizz(testdb):
    """Quizz test object"""
    _, connection, _ = testdb
    return Quizz(connection)


@pytest.fixture
def question():
    """Default question and answers"""
    return 'what is your quest?', ['to seek the Holy Grail']


def test_add_question(quizz, question):
    """Add a question"""
    que, ans = question
    quizz.add_question(que, ans)
    assert len(quizz.questions) == 1


def test_add_accented_question(quizz):
    """Add a question containing accented chars"""
    quizz.add_question('åéàè', ['ïùø', 'çīł'])
    assert len(quizz.questions) == 1


def test_add_unicode_question(quizz):
    """Add a question containing accented chars (unicode)"""
    quizz.add_question(u'åéàè', [u'ïùø', u'çīł'])
    assert len(quizz.questions) == 1


def test_add_empty_question(quizz, question):
    """Attempt to add an empty question"""
    _, ans = question
    with pytest.raises(ValueError):
        quizz.add_question('', ans)
    with pytest.raises(ValueError):
        quizz.add_question(None, ans)


def test_add_empty_answers(quizz, question):
    """Attempt to add a question with no answers"""
    que, _ = question
    with pytest.raises(ValueError):
        quizz.add_question(que, [])
    with pytest.raises(ValueError):
        quizz.add_question(que, [''])
    with pytest.raises(ValueError):
        quizz.add_question(que, None)


def test_repr(quizz, question):
    """Display quizz questions as a string"""
    que, ans = question
    quizz.add_question(que, ans)
    assert str(quizz) == '1 - what is your quest?'

    quizz.add_question(
        'what is the capital of Assyria?',
        ['Assur', 'Ashur', u'Aššur']
    )
    assert str(quizz) == \
        '1 - what is your quest?\n2 - what is the capital of Assyria?'


def test_delete_question(quizz, question):
    """Add and delete a question"""
    # pylint: disable=len-as-condition
    que, ans = question
    quizz.add_question(que, ans)
    assert len(quizz.questions) == 1

    quizz.delete_question(1)
    assert len(quizz.questions) == 0


def test_check_answer(quizz):
    """What is your favorite color?"""
    quizz.add_question('what is your favorite color?', ['blue', 'blue.'])
    quizz.ask_next_question()
    assert quizz.check_answer('Blue.')
    assert quizz.check_answer('blue')
    assert quizz.check_answer('bLuE')
    assert quizz.check_answer('Blue. No yel--') is False
