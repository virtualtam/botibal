# -*- coding: utf-8 -*-
'Quizzibal: a silly XMPP quizz bot'
import re

from botibal.client.minibal import MiniBal
from botibal.quizz import Quizz, ScoreDict


class QuizziBal(MiniBal):
    'A quizzical XMPP bot'
    # pylint: disable=too-many-public-methods

    def __init__(self, jid, password, nick, room, admin_jid):
        # pylint: disable=too-many-arguments
        super(QuizziBal, self).__init__(jid, password, nick, room, admin_jid)
        self.quizz = Quizz(self.db_conn)
        self.scores = ScoreDict()
        self.adding_question = False
        self.running = False

    def message(self, msg):
        # pylint: disable=duplicate-code
        if msg['mucnick'] == self.nick:
            return

        if msg['type'] not in ('chat', 'normal'):
            return

        super(QuizziBal, self).message(msg)

        cmd, args = self.parse_user_command(msg)
        if cmd is None:
            return

        if cmd == 'q_add':
            q_set = args.split('#')
            self.quizz.add_question(q_set[0], q_set[1:])
            msg.reply('Question added: {}\nAnswers: {}'
                      .format(q_set[0], q_set[1:])).send()

        elif cmd == 'q_del':
            msg.reply(self.quizz.delete_question(int(args))).send()

        elif cmd == 'q_list':
            msg.reply(str(self.quizz)).send()

    def muc_message(self, msg):
        if msg['mucnick'] == self.nick:
            return

        super(QuizziBal, self).muc_message(msg)

        self.say_group(self.control(msg))

    def add_question(self, message):
        'Adds a new quizz question'
        lines = message.getBody().splitlines()
        return self.quizz.add_question(lines[0], lines[1:])


    def check_answer(self, matchobject, username):
        'Handles user answers'
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


    def control(self, msg):
        'Starts and stops quizz sessions'
        cmd, _ = self.parse_muc_command(msg)
        if cmd is None:
            return

        result = ''

        if cmd == 'next':
            result = self.quizz.ask_next_question()

        elif cmd == 'reset':
            self.scores.reset()
            result = 'All scores have been reset!'

        elif cmd == 'score':
            result = self.scores.results()

        elif cmd == 'start':
            if self.running:
                return 'The quizz is already running ^_^'

            self.running = True
            result = self.quizz.ask_next_question()

        elif cmd == 'stop':
            self.running = False
            result = "Quizz stopped"

        else:
            if not self.running:
                return

            # check an answer
            matches = re.search(
                "^(" + self.nick +
                r")(( )?(: |, )?)((\w| |[\.,:éèçàêâûîôäëüïö'])+)",
                msg['body'])
            if matches:
                result = self.check_answer(matches, msg['mucnick'])

        return result
