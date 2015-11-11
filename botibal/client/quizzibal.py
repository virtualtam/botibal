# -*- coding: utf-8 -*-
"""
Quizzibal: a silly XMPP quizz bot
"""
import re

from botibal.client.cmd_parser import BotCmdError, BotHelp
from botibal.client.minibal import MiniBal
from botibal.quizz import Quizz, ScoreDict


class QuizziBal(MiniBal):
    """
    A quizzical XMPP bot
    """

    # pylint: disable=too-many-public-methods

    def __init__(self, jid, password, nick, room, admin_jid,
                 database='data.db'):
        # pylint: disable=too-many-arguments
        super(QuizziBal, self).__init__(
            jid, password, nick, room, admin_jid, database)
        self.quizz = Quizz(self.db_conn)
        self.scores = ScoreDict()
        self.running = False

    def check_answer(self, matchobject, username):
        """
        Handles user answers
        """
        if not self.running:
            return 'Sorry, there is no quizz running'

        answer = matchobject.group(5)
        if self.quizz.check_answer(answer):
            self.scores.add_score(username, 1)
            return 'Good answer {}!\nYou now have {} points\n'\
                'Next question: {}'.format(
                    username, self.scores[username],
                    self.quizz.ask_next_question())

        return "Sorry {}, {} is not the answer to my question.".format(
            username, answer)

    def question(self, msg, args):
        """
        Manages quizz questions
        """
        if args.add:
            q_set = (' '.join(args.add)).split('#')
            try:
                self.quizz.add_question(q_set[0], q_set[1:])
                self.send_reply(msg, 'Question added: {}\nAnswers: {}'
                                .format(q_set[0], q_set[1:]))
            except ValueError as err:
                self.send_reply(msg, 'error: {}'.format(err))

        elif args.delete:
            self.send_reply(msg, self.quizz.delete_question(int(args.delete)))

        elif args.list:
            self.send_reply(msg, '\n{}'.format(self.quizz))

    def control_quizz(self, msg, args):
        """
        Controls the running quizz
        """
        if args.action == 'next':
            self.say_group(self.quizz.ask_next_question())

        elif args.action == 'reset':
            self.scores.reset()
            self.say_group('All scores have been reset!')

        elif args.action == 'score':
            self.send_reply(msg, '\nScores:\n{}'.format(self.scores.results()))

        elif args.action == 'start':
            if self.running:
                self.send_reply(msg, 'The quizz is already running ^_^')
                return

            self.running = True
            self.say_group(self.quizz.ask_next_question())

        elif args.action == 'stop':
            self.running = False
            self.say_group('Quizz stopped')

    def add_message_commands(self, subparser):
        super(QuizziBal, self).add_message_commands(subparser)

        p_que = subparser.add_parser('question', help='manage quizz questions')
        p_que.add_argument('-a', '--add', type=str, nargs='+',
                           help='add a new question to the quizz')
        p_que.add_argument(
            '-d', '--delete', type=int,
            help='delete the question corresponding to the given ID')
        p_que.add_argument('-l', '--list', action='store_true',
                           help='lists all questions')
        p_que.set_defaults(func=self.question)

        p_quizz = subparser.add_parser('quizz', help='control quizzes')
        p_quizz.add_argument(
            'action', help='control action',
            choices=['next', 'reset', 'score', 'start', 'stop'])
        p_quizz.set_defaults(func=self.control_quizz)

    def muc_hook(self, msg):
        super(QuizziBal, self).muc_hook(msg)

        if not self.running:
            return False

        # check if the answer is a valid command
        try:
            cmdline = re.sub(r'{}[ ]?[,:]? '.format(self.nick), '',
                             msg['body'])
            self.muc_cmd_parser.parse_args(cmdline.split(' '))

        except BotHelp:
            # user asked for help: proceed
            return False

        except BotCmdError:
            # not a valid command: check as an answer
            matches = re.search(
                r"^(" + self.nick +
                r")(( )?(: |, )?)((\w| |[\.,:éèçàêâûîôäëüïö'])+)",
                msg['body'])
            if matches:
                self.say_group(self.check_answer(matches, msg['mucnick']))
            return True

        # user emitted a valid command: proceed
        return False
