# -*- coding: utf-8 -*-
# pylint: disable=too-many-public-methods
"""
Tests the quizz module
"""
from __future__ import unicode_literals

import unittest

from botibal.quizz import Quizz, ScoreDict
from tests.utils import DBTestCase


class TestScoreDict(unittest.TestCase):
    """
    Handles quizz scores
    """

    def setUp(self):
        self.scores = ScoreDict()

    def test_add_score(self):
        """
        Add a new score
        """
        self.scores.add_score('Luke', 1)
        self.assertEqual(self.scores['Luke'], 1)

    def test_add_string_score(self):
        """
        Add a new score: integer represented as a string
        """
        self.scores.add_score('Luke', '10')
        self.assertEqual(self.scores['Luke'], 10)

    def test_add_invalid_score(self):
        """
        Attempt to add a string
        """
        with self.assertRaises(ValueError):
            self.scores.add_score('Luke', 'Use the Force')

    def test_increment_score(self):
        """
        Wow, that guy is good! Look, he scored, twice!
        """
        self.scores.add_score('Luke', 1)
        self.assertEqual(self.scores['Luke'], 1)
        self.scores.add_score('Luke', 1)
        self.assertEqual(self.scores['Luke'], 2)

    def test_reset(self):
        """
        Re-settle the scores!
        """
        self.scores.add_score('Luke', 7)
        self.scores.add_score('Vader', 5)
        self.scores.reset()
        self.assertEqual(self.scores['Luke'], 0)
        self.assertEqual(self.scores['Vader'], 0)

    def test_results(self):
        """
        Display the scores as a string
        """
        self.scores.add_score('Luke', 1)
        self.assertEqual(self.scores.results(), 'Luke: 1')

        self.scores.add_score('Luke', 3)
        self.scores.add_score('Vader', 333)
        self.assertEqual(self.scores.results(), 'Luke: 4\nVader: 333')

        self.scores.add_score('Vader', 333)
        self.assertEqual(self.scores.results(), 'Luke: 4\nVader: 666')


class TestQuizz(DBTestCase):
    """
    Covers Quizz methods
    """

    @classmethod
    def setUpClass(cls):
        cls.question = 'what is your quest?'
        cls.answers = ['to seek The Holy Grail']

    def setUp(self):
        super(TestQuizz, self).setUp()
        self.qzz = Quizz(self.db_conn)

    def test_add_question(self):
        """
        Add a question
        """
        self.qzz.add_question(self.question, self.answers)
        self.assertEqual(len(self.qzz.questions), 1)

    def test_add_accented_question(self):
        """
        Add a question containing accented chars
        """
        self.qzz.add_question('åéàè', ['ïùø', 'çīł'])
        self.assertEqual(len(self.qzz.questions), 1)

    def test_add_unicode_question(self):
        """
        Add a question containing accented chars (unicode)
        """
        self.qzz.add_question(u'åéàè', [u'ïùø', u'çīł'])
        self.assertEqual(len(self.qzz.questions), 1)

    def test_add_empty_question(self):
        """
        Attempt to add an empty question
        """
        with self.assertRaises(ValueError):
            self.qzz.add_question('', self.answers)
        with self.assertRaises(ValueError):
            self.qzz.add_question(None, self.answers)

    def test_add_empty_answers(self):
        """
        Attempt to add a question with no answers
        """
        with self.assertRaises(ValueError):
            self.qzz.add_question(self.question, [])
        with self.assertRaises(ValueError):
            self.qzz.add_question(self.question, [''])
        with self.assertRaises(ValueError):
            self.qzz.add_question(self.question, None)

    def test_repr(self):
        """
        Display quizz questions as a string
        """
        self.qzz.add_question(self.question, self.answers)
        self.assertEqual(str(self.qzz), '1 - what is your quest?')
        self.qzz.add_question('what is the capital of Assyria?',
                              ['Assur', 'Ashur', u'Aššur'])
        self.assertEqual(str(self.qzz),
                         '1 - what is your quest?\n'
                         '2 - what is the capital of Assyria?')

    def test_delete_question(self):
        """
        Add and delete a question
        """
        self.qzz.add_question(self.question, self.answers)
        self.assertEqual(len(self.qzz.questions), 1)
        self.qzz.delete_question(1)
        self.assertEqual(len(self.qzz.questions), 0)

    def test_check_answer(self):
        """
        What is your favorite color?
        """
        self.qzz.add_question('what is your favorite color?',
                              ['blue', 'blue.'])
        self.qzz.ask_next_question()
        self.assertTrue(self.qzz.check_answer('Blue.'))
        self.assertTrue(self.qzz.check_answer('blue'))
        self.assertTrue(self.qzz.check_answer('bLuE'))
        self.assertFalse(self.qzz.check_answer('Blue. No yel--'))


if __name__ == '__main__':
    unittest.main()
