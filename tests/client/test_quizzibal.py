# -*- coding: utf-8 -*-
'botibal.client.quizzibal unit tests'
# pylint: disable=too-many-public-methods
import unittest

from sleekxmpp.stanza import Message

from botibal.client.quizzibal import QuizziBal

from tests.client.utils import MockMiniBal, ClientTestCase


class MockQuizziBal(QuizziBal, MockMiniBal):
    'Mock client for local testing'


class TestQuizziBal(ClientTestCase):
    'Covers command parsing'

    @classmethod
    def setUpClass(cls):
        cls.que = 'q?#a1#a2#a3'

    def setUp(self):
        super(TestQuizziBal, self).setUp()
        self.client = MockQuizziBal('bot@server.org', 'p455w0rd', 'bot',
                                    'room@server.org', 'admin@server.org',
                                    self.test_db)

    def test_init(self):
        'Build-Bot :-)'
        QuizziBal('bot@server.org', 'p455w0rd', 'bot',
                  'room@server.org', 'admin@server.org', self.test_db)

    def test_question_add(self):
        'Add a question'
        self.client.question(Message(),
                             self._parse_cmd('question -a {}'.format(self.que)))
        self.assertReplyEqual("Question added: q?\nAnswers: ['a1', 'a2', 'a3']")

    def test_question_add_duplicate(self):
        'Add a question. Twice.'
        # TODO: prevent adding duplicates
        pass

    def test_question_add_error(self):
        'Add a question with no answers'
        args = self._parse_cmd('question -a q?#')

        self.client.question(Message(), args)
        self.assertReplyEqual('error: No answers specified')

    def test_question_list(self):
        'List questions'
        self.client.quizz.add_question('q1?', ['a1'])
        self.client.quizz.add_question('q2?', ['a2'])
        self.client.question(Message(), self._parse_cmd('question -l'))
        self.assertReplyEqual('\n1 - q1?\n2 - q2?')

    def test_question_del(self):
        'Delete a question'
        self.client.quizz.add_question('q1?', ['a1'])
        self.client.quizz.add_question('q2?', ['a2'])
        self.client.question(Message(), self._parse_cmd('question -d 2'))
        self.assertEqual(str(self.client.quizz), '1 - q1?')
        self.assertReplyEqual('The question #2 has been deleted')

    def test_control_next(self):
        'Skip the question'
        pass

    def test_control_reset(self):
        'Reset the scores'
        pass

    def test_control_score(self):
        'Display current scores'
        pass

    def test_control_start(self):
        'Start the quizz'
        pass

    def test_control_start_bis(self):
        'Start the quizz. Twice.'
        pass

    def test_control_stop(self):
        'Stop the quizz'
        pass

    def test_check_good_answer(self):
        'Someone has given the right answer'
        pass

    def test_check_wrong_answer(self):
        'Someone has given the wrong answer'
        pass


if __name__ == '__main__':
    unittest.main()
