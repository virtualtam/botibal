# -*- coding: utf-8 -*-
"""
botibal.client.quizzibal unit tests
"""
# pylint: disable=too-many-public-methods
import re
import unittest

from botibal.client.quizzibal import QuizziBal
from tests.client.utils import ClientTestCase, MockMiniBal

try:
    from sleekxmpp.stanza import Message
except ImportError:
    # pylint: disable=import-error
    from slixmpp.stanza import Message


class MockQuizziBal(QuizziBal, MockMiniBal):
    """
    Mock client for local testing
    """


class TestQuizziBal(ClientTestCase):
    """
    Covers command parsing
    """

    @classmethod
    def setUpClass(cls):
        cls.que = 'q?#a1#a2#a3'

    def setUp(self):
        super(TestQuizziBal, self).setUp()
        self.client = MockQuizziBal('bot@server.org', 'p455w0rd', 'bot',
                                    'room@server.org', 'admin@server.org',
                                    self.test_db)

    def _check_answer(self, answer, nick):
        """
        Wraps answer checking
        """
        matches = re.search(
            r"^(" + self.client.nick +
            r")(( )?(: |, )?)((\w| |[\.,:éèçàêâûîôäëüïö'])+)",
            '{}: {}'.format(self.client.nick, answer))
        return self.client.check_answer(matches, nick)

    def test_init(self):
        """
        Build-Bot :-)
        """
        QuizziBal('bot@server.org', 'p455w0rd', 'bot',
                  'room@server.org', 'admin@server.org', self.test_db)

    def test_question_add(self):
        """
        Add a question
        """
        self.client.question(Message(),
                             self._parse_cmd('question -a {}'.format(self.que)))
        self.assertReplyEqual("Question added: q?\nAnswers: ['a1', 'a2', 'a3']")

    def test_question_add_duplicate(self):
        """
        Add a question. Twice.
        """
        self.client.question(Message(),
                             self._parse_cmd('question -a {}'.format(self.que)))
        self.assertReplyEqual("Question added: q?\nAnswers: ['a1', 'a2', 'a3']")
        self.client.question(Message(),
                             self._parse_cmd('question -a {}'.format(self.que)))
        self.assertReplyEqual('error: Duplicate question')

    def test_question_add_error(self):
        """
        Add a question with no answers
        """
        args = self._parse_cmd('question -a q?#')

        self.client.question(Message(), args)
        self.assertReplyEqual('error: No answers specified')

    def test_question_list(self):
        """
        List questions
        """
        self.client.quizz.add_question('q1?', ['a1'])
        self.client.quizz.add_question('q2?', ['a2'])
        self.client.question(Message(), self._parse_cmd('question -l'))
        self.assertReplyEqual('\n1 - q1?\n2 - q2?')

    def test_question_del(self):
        """
        Delete a question
        """
        self.client.quizz.add_question('q1?', ['a1'])
        self.client.quizz.add_question('q2?', ['a2'])
        self.client.question(Message(), self._parse_cmd('question -d 2'))
        self.assertEqual(str(self.client.quizz), '1 - q1?')
        self.assertReplyEqual('The question #2 has been deleted')

    def test_control_next(self):
        """
        Skip the question
        """
        # add and ask a first question
        self.client.quizz.add_question('q1?', ['a1'])
        self.client.control_quizz(Message(), self._parse_cmd('quizz start'))
        self.assertTrue(self.client.running)
        self.assertSayGroupEqual('q1?')

        # remove it
        self.client.quizz.delete_question(1)

        # add and ask a second question
        self.client.quizz.add_question('q2?', ['a2'])
        self.client.control_quizz(Message(), self._parse_cmd('quizz next'))
        self.assertSayGroupEqual('q2?')

    def test_control_reset(self):
        """
        Reset the scores
        """
        self.client.control_quizz(Message(), self._parse_cmd('quizz reset'))
        self.assertSayGroupEqual('All scores have been reset!')

    def test_control_score(self):
        """
        Display current scores
        """
        self.client.control_quizz(Message(), self._parse_cmd('quizz score'))
        self.assertReplyEqual('\nScores:\n')

    def test_control_start(self):
        """
        Start the quizz
        """
        self.client.quizz.add_question('q1?', ['a1'])
        self.client.control_quizz(Message(), self._parse_cmd('quizz start'))
        self.assertTrue(self.client.running)
        self.assertSayGroupEqual('q1?')

    def test_control_start_bis(self):
        """
        Start the quizz. Twice.
        """
        self.client.quizz.add_question('q1?', ['a1'])
        self.client.control_quizz(Message(), self._parse_cmd('quizz start'))
        self.assertTrue(self.client.running)
        self.assertSayGroupEqual('q1?')
        self.client.control_quizz(Message(), self._parse_cmd('quizz start'))
        self.assertTrue(self.client.running)
        self.assertReplyEqual('The quizz is already running ^_^')

    def test_control_stop(self):
        """
        Stop the quizz
        """
        self.client.quizz.add_question('q1?', ['a1'])
        self.client.control_quizz(Message(), self._parse_cmd('quizz start'))
        self.assertTrue(self.client.running)
        self.client.control_quizz(Message(), self._parse_cmd('quizz stop'))
        self.assertFalse(self.client.running)

    def test_check_answer_no_quizz(self):
        """
        You're asking me answers, but you already know the question!
        """
        self.assertEqual(self._check_answer('You know nothing, Jones No', None),
                         'Sorry, there is no quizz running')

    def test_check_good_answer(self):
        """
        Someone has given the right answer
        """
        self.client.quizz.add_question('q1?', ['a1'])
        self.client.control_quizz(Message(), self._parse_cmd('quizz start'))
        self.assertEqual(self._check_answer('a1', 'Hans'),
                         'Good answer Hans!\nYou now have 1 points\n'
                         'Next question: q1?')

    def test_check_wrong_answer(self):
        """
        Someone has given the wrong answer
        """
        self.client.quizz.add_question('q1?', ['a1'])
        self.client.control_quizz(Message(), self._parse_cmd('quizz start'))
        self.assertEqual(self._check_answer('1a', 'Hans'),
                         'Sorry Hans, 1a is not the answer to my question.')


if __name__ == '__main__':
    unittest.main()
