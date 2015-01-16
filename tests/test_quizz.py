# -*- coding: utf-8 -*-
# pylint: disable=too-many-public-methods
'Tests the quizz module'
import os
import unittest
from minibal.quizz import Question, Quizz


TEST_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_QUIZZ_DIR = os.path.join(TEST_DIR, 'quizz')


class TestQuestion(unittest.TestCase):
    'Covers Question methods'
    @classmethod
    def setUpClass(cls):
        cls.question = 'what is your favorite color?'
        cls.answers = ['blue', 'blue.']
        cls.filepath = os.path.join(TEST_QUIZZ_DIR, 'keeper.quizz')
        cls.que = Question(cls.question, cls.answers, cls.filepath)


    def test_save_to_file(self):
        'Ensure we correctly write the question in a file'
        if os.path.isfile(self.filepath):
            os.remove(self.filepath)
        self.que.save_to_file()

        with open(self.filepath) as f_question:
            lines = f_question.read().splitlines()
        os.remove(self.filepath)

        self.assertEqual(lines[0], self.question)
        for index in range(1, len(lines)):
            self.assertEqual(lines[index], self.answers[index - 1])


    def test_check_answer(self):
        'What is your favorite color?'
        self.assertTrue(self.que.check_answer('Blue.'))
        self.assertTrue(self.que.check_answer('blue'))
        self.assertTrue(self.que.check_answer('bLuE'))
        self.assertFalse(self.que.check_answer('Blue.  No yel--'))



class TestQuizz(unittest.TestCase):
    'Covers Quizz methods'
    @classmethod
    def setUpClass(cls):
        cls.question = 'what is your quest?'
        cls.answers = ['to seek The Holy Grail']
        cls.filepath = os.path.join(TEST_QUIZZ_DIR, 'keeper.2.qzz')


    def setUp(self):
        if os.path.isfile(self.filepath):
            os.remove(self.filepath)
        self.qzz = Quizz(TEST_QUIZZ_DIR)


    def test_load_from_dir(self):
        'Load the questions/answers from quizz files'
        self.assertEqual(len(self.qzz.questions), 2)
        self.assertEqual(self.qzz.questions[0].question, 'quel est le muscle ?')
        self.assertEqual(self.qzz.questions[1].question,
                         'how many meals does a Hobbit eat per day?')


    def test_add_question(self):
        'Add a question (saved to a file)'
        self.qzz.add_question(self.question, self.answers, self.filepath)
        self.assertEqual(len(self.qzz.questions), 3)
        self.assertTrue(os.path.isfile(self.filepath))


    def test_delete_question(self):
        'Add and delete a question'
        self.qzz.add_question(self.question, self.answers, self.filepath)
        self.assertEqual(len(self.qzz.questions), 3)
        self.assertTrue(os.path.isfile(self.filepath))
        self.qzz.delete_question(2)
        self.assertEqual(len(self.qzz.questions), 2)
        self.assertFalse(os.path.isfile(self.filepath))


if __name__ == '__main__':
    unittest.main()
