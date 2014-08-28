#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'Quizzibal: a silly jabber quizz bot'
import datetime
import os
import re
import sys
from minibal import MiniBal
from quizz import Quizz, QUIZZ_DIR
import config


# pylint: disable=too-many-public-methods
class QuizziBal(MiniBal):
    'A jabber bot dedicated to quizzes'

    def __init__(self, jid, password, nickname, admin_jid):
        super(QuizziBal, self).__init__(jid, password, nickname, admin_jid)
        self.quizz = Quizz()
        self.scores = dict()
        self.current_question = None
        self.adding_question = False
        self.running = False


    def unknown_command(self, mess, cmd, args):
        # add a new question
        if self.adding_question and mess.getType() == 'chat':
            self.adding_question = False
            return self.add_question(mess)

        if re.search('^add$', mess.getBody()) and mess.getType() == 'chat':
            self.adding_question = True
            return 'Please type your question and its answers'

        # start/stop the quizz, display scores, skip the question
        matches = re.search("^(" + self.nickname +\
                            ")(( )?(: |, )?)(start|stop|score|next)|reset",
                            mess.getBody())
        if matches:
            return self.control(matches)

        # check an answer
        matches = re.search("^(" + self.nickname +\
                            r")(( )?(: |, )?)((\w| |[\.,:éèçàêâûîôäëüïö'])+)",
                            mess.getBody())
        if matches:
            return self.check_answer(matches, self.get_sender_username(mess))

        # list available questions
        if re.search('^list$', mess.getBody()):
            return self.quizz.list_questions()


        # delete a question
        matches = re.search('^del ([1-9][0-9]*)', mess.getBody())
        if matches:
            return self.quizz.delete_question(int(matches.group(1)))


    def add_question(self, message):
        'Adds a new quizz question'
        filepath = os.path.join(
            QUIZZ_DIR,
            '{}.{}.qzz'.format(
                self.get_sender_username(message),
                datetime.datetime.now().strftime('%Y%m%d_%H%M%S')))

        lines = message.getBody().splitlines()
        return self.quizz.add_question(lines[0], lines[1:], filepath)


    def display_scores(self):
        'Displays the scores'
        return '\n'.join(['{}: {}'.format(user, score)
                          for user, score in self.scores.items()])


    def reset_scores(self):
        'Resets all scores'
        self.scores = dict()
        return 'All scores have been reset!'


    def check_answer(self, matchobject, username):
        'Handles user answers'
        if not self.running:
            return 'Sorry, there is no quizz running'

        answer = matchobject.group(5)
        if self.quizz.check_answer(answer):
            if username in self.scores:
                self.scores[username] += 1
            else:
                self.scores[username] = 1

            return "Good answer {}!\nYou have now {} points\n"\
                "Next question: {}".format(
                    username, self.scores[username],
                    self.ask_next_question())

        return "Sorry {}, {} is not the answer to my question.".format(
            username, answer)


    def control(self, matchobject):
        'Starts and stops quizz sessions'
        msg = matchobject.group(5)

        if msg == "start" and self.running is False:
            self.running = True

            if not os.access(QUIZZ_DIR, os.F_OK):
                return "Quizz directory does not exist, cannot proceed"

            return self.ask_next_question()

        if msg == "stop":
            self.running = False
            return "Quizz stopped"

        if msg == "score":
            return self.display_scores()

        if msg == 'reset':
            return self.reset_scores()

        if msg == "next":
            return self.ask_next_question()


    def ask_next_question(self):
        'Asks the next question'
        return self.quizz.ask_next_question()


if __name__ == '__main__':
    #dirty fix, but needed to use unicode…
    reload(sys)
    sys.setdefaultencoding("utf-8")
    BOT = QuizziBal(config.JID, config.PASSWORD, 'Quizzibal', config.ADMIN_JID)
    BOT.serve_forever()
