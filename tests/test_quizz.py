# -*- coding: utf-8 -*-
# pylint: disable=too-many-public-methods
'Tests the quizz module'
import unittest
from botibal.quizz import Quizz
from tests.utils import DBTestCase


class TestQuizz(DBTestCase):
    'Covers Quizz methods'
    @classmethod
    def setUpClass(cls):
        cls.question = 'what is your quest?'
        cls.answers = ['to seek The Holy Grail']

    def setUp(self):
        super(TestQuizz, self).setUp()
        self.qzz = Quizz(self.db_conn)

    def test_add_question(self):
        'Add a question'
        self.qzz.add_question(self.question, self.answers)
        self.assertEqual(len(self.qzz.questions), 1)

    def test_add_empty_question(self):
        'Attempt to add an empty question'
        with self.assertRaises(ValueError):
            self.qzz.add_question('', self.answers)
        with self.assertRaises(ValueError):
            self.qzz.add_question(None, self.answers)

    def test_add_empty_answers(self):
        'Attempt to add a question with no answers'
        with self.assertRaises(ValueError):
            self.qzz.add_question(self.question, [])
        with self.assertRaises(ValueError):
            self.qzz.add_question(self.question, [''])
        with self.assertRaises(ValueError):
            self.qzz.add_question(self.question, None)

    def test_delete_question(self):
        'Add and delete a question'
        self.qzz.add_question(self.question, self.answers)
        self.assertEqual(len(self.qzz.questions), 1)
        self.qzz.delete_question(1)
        self.assertEqual(len(self.qzz.questions), 0)

    def test_check_answer(self):
        'What is your favorite color?'
        self.qzz.add_question('what is your favorite color?',
                              ['blue', 'blue.'])
        self.qzz.ask_next_question()
        self.assertTrue(self.qzz.check_answer('Blue.'))
        self.assertTrue(self.qzz.check_answer('blue'))
        self.assertTrue(self.qzz.check_answer('bLuE'))
        self.assertFalse(self.qzz.check_answer('Blue. No yel--'))


if __name__ == '__main__':
    unittest.main()
