#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'Quizzibal: a silly jabber quizz bot'
import time
import re
import random
import os
import sys
from minibal import MiniBal
import config


# pylint: disable=too-many-public-methods
class QuizziBal(MiniBal):
    'A jabber bot dedicated to quizzes'

    current_file = 0
    current_question = list()
    question_asked = False
    question_done = list()
    scores = dict()
    quizz_mode = False

    adding_question = False
    current_question_file_added = ""

    def unknown_command(self, mess, cmd, args):
        matches = re.search("^(" + self.nickname +\
                            ")(( )?(: |, )?)(start|stop|score|next)",
                            mess.getBody())
        if matches:
            return self.quizzHandler(matches)
        else:
            matches = re.search("^(" + self.nickname +\
                                r")(( )?(: |, )?)((\w| |[éèçàêâûîôäëüïö'])+)",
                                mess.getBody())
            if matches:
                return self.quizzAnswerHandler(matches,
                                               self.get_sender_username(mess))
            else:
                matches = re.search("^question add$", mess.getBody())

                if matches and mess.getType() == "chat"\
                   and self.adding_question == False:
                    return self.questionAdder(mess, "prequestion")
                else:
                    if self.adding_question and mess.getType() == "chat":
                        return self.questionAdder(mess, "question")

    def questionAdder(self, message, state):
        'Adds a new quizz question'
        if state == "prequestion":
            self.adding_question = True
            text = 'Enter your question, in a single message {}.\n'\
                   'Do not forget the template\n:'.format(
                       self.get_sender_username(message))
            text += "Question sur une seule ligne, sans faute d'orthographe "\
                    "si possible ?\nreponse possible (sur une seule ligne, "\
                    "la casse n'est pas prise en compte)\nautre reponse "\
                    "possible (par le bot, donc pas la peine de faire une "\
                    "ligne par)\nitou (variation possible de casse)\nde même\n"\
                    "ditto\ntoujours pareil\netc\ntoossa"
            return text
        else:
            if state == "question":
                if self.current_question_file_added == "":
                    self.current_question_file_added = "{}/{}.{}.quizz".format(
                        QUIZZ_DIR,
                        self.get_sender_username(message),
                        time.time())
                    with open(self.current_question_file_added, 'a')\
                         as f_question:
                        f_question.write(message.getBody()+"\n")

                    self.adding_question = False
                    self.current_question_file_added = ""
                    return "Your question has been successfully added, "\
                        "{}".format(self.get_sender_username(message))

    def quizzScoreHandler(self):
        'Displays the scores'
        msg = ""
        for i in self.scores.keys():
            msg += i +': %d\n' % (self.scores[i])
        return msg

    def quizzAnswerHandler(self, matchobject, username):
        'Handles user answers'
        if self.question_asked:
            answer = matchobject.group(5)
            for i in range(1, len(self.current_question)):
                if re.match(answer, self.current_question[i], re.IGNORECASE):
                    if username in self.scores:
                        self.scores[username] += 1
                    else:
                        self.scores[username] = 1

                    self.question_asked = False
                    return "Good answer {}!\nYou have now {} points\n"\
                        "Next question: {}".format(
                            username, self.scores[username],
                            self.askNextQuestion())

            return "Sorry {}, {} is not the answer to my question.".format(
                username, answer)
        else:
            return "Sorry, the answer to this question has already been given "\
                "or there is no question running"

    def quizzHandler(self, matchobject):
        'Starts and stops quizz sessions'
        msg = matchobject.group(5)
        if msg == "start" and not self.quizz_mode:
            self.quizz_mode = True
            if self.quizz_mode and os.access(QUIZZ_DIR, os.F_OK)\
               and not self.question_asked:
                return self.askNextQuestion()
            else:
                self.quizz_mode = False
                return "Quizz directory does not exist, cannot proceed"
        else:
            if msg == "stop":
                self.quizz_mode = False
                return "Quizz stopped"
            else:
                if msg == "score":
                    return self.quizzScoreHandler()
                else:
                    if msg == "next" and not self.question_asked:
                        return self.askNextQuestion()

    def askNextQuestion(self):
        'Asks the next question'
        quizz_files = os.listdir(QUIZZ_DIR)
        if len(quizz_files) == len(self.question_done):
            del self.question_done[:]

        index = random.randint(0, len(quizz_files)-1)
        while index in self.question_done:
            index = random.randint(0, len(quizz_files)-1)

        with open(QUIZZ_DIR + "/" + quizz_files[index], "r") as f_question:
            self.current_question = f_question.readlines()

        self.question_asked = True
        self.question_done.append(index)
        return self.current_question[0]


if __name__ == '__main__':
    #dirty fix, but needed to use unicode…
    reload(sys)
    sys.setdefaultencoding("utf-8")
    BOT = QuizziBal(config.JID, config.PASSWORD, 'Quizzibal', config.ADMIN_JID)
    BOT.serve_forever()
