#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'Quizzibal: a silly jabber quizz bot'
from jabberbot import JabberBot, botcmd
import xmpp
import time
import re
import random
import os
import sys
import config


class Quizzibal(JabberBot):
    'A jabber bot dedicated to quizzes'

    __groupchat = None
    __nickname = 'Quizzibal'
    __jid = config.JID
    __password = config.PASSWORD
    __admin_jid = config.ADMIN_JID

    __quizzDir = "quizz"
    __currentFile = 0
    __currentQuestion = list()
    __questionAsked = False
    __questionDone = list()
    __score = dict()
    __quizzMode = False

    __addingQuestion = False
    __currentQuestionFileAdded = ""

    def __init__(self):
        super(Quizzibal, self).__init__(self.__jid, self.__password)

    def join_room(self, room):
        """Join the specified multi-user chat room"""
        room_jid = "%s/%s" % (room, self.__nickname)
        self.connect().send(xmpp.Presence(to=room_jid))

    def unknown_command(self, mess, cmd, args):
        matches = re.search("^(" + self.__nickname +\
                            ")(( )?(: |, )?)(start|stop|score|next)",
                            mess.getBody())
        if matches:
            return self.quizzHandler(matches)
        else:
            matches = re.search("^(" + self.__nickname +\
                                ")(( )?(: |, )?)((\w| |[éèçàêâûîôäëüïö'])+)",
                                mess.getBody())
            if matches:
                return self.quizzAnswerHandler(matches,
                                               self.get_sender_username(mess))
            else:
                matches = re.search("^question add$", mess.getBody())

                if matches and mess.getType() == "chat"\
                   and self.__addingQuestion == False:
                    return self.questionAdder(mess, "prequestion")
                else:
                    if self.__addingQuestion and mess.getType() == "chat":
                        return self.questionAdder(mess, "question")

    def questionAdder(self, message, state):
        'Adds a new quizz question'
        if state == "prequestion":
            self.__addingQuestion = True
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
                if self.__currentQuestionFileAdded == "":
                    self.__currentQuestionFileAdded = "{}/{}.{}.quizz".format(
                        self.__quizzDir,
                        self.get_sender_username(message),
                        time.time())
                    with open(self.__currentQuestionFileAdded, 'a')\
                         as f_question:
                        f_question.write(message.getBody()+"\n")

                    self.__addingQuestion = False
                    self.__currentQuestionFileAdded = ""
                    return "Your question has been successfully added, "\
                        "{}".format(self.get_sender_username(message))

    def quizzScoreHandler(self):
        'Displays the scores'
        msg = ""
        for i in self.__score.keys():
            msg += i +': %d\n' % (self.__score[i])
        return msg

    def quizzAnswerHandler(self, matchobject, username):
        'Handles user answers'
        if self.__questionAsked:
            answer = matchobject.group(5)
            for i in range(1, len(self.__currentQuestion)):
                if re.match(answer, self.__currentQuestion[i], re.IGNORECASE):
                    if username in self.__score:
                        self.__score[username] += 1
                    else:
                        self.__score[username] = 1

                    self.__questionAsked = False
                    return "Good answer {}!\nYou have now {} points\n"\
                        "Next question: {}".format(
                            username, self.__score[username],
                            self.askNextQuestion())

            return "Sorry {}, {} is not the answer to my question.".format(
                username, answer)
        else:
            return "Sorry, the answer to this question has already been given "\
                "or there is no question running"

    def quizzHandler(self, matchobject):
        'Starts and stops quizz sessions'
        msg = matchobject.group(5)
        if msg == "start" and not self.__quizzMode:
            self.__quizzMode = True
            if self.__quizzMode and os.access(self.__quizzDir, os.F_OK)\
               and not self.__questionAsked:
                return self.askNextQuestion()
            else:
                self.__quizzMode = False
                return "Quizz directory does not exist, cannot proceed"
        else:
            if msg == "stop":
                self.__quizzMode = False
                return "Quizz stopped"
            else:
                if msg == "score":
                    return self.quizzScoreHandler()
                else:
                    if msg == "next" and not self.__questionAsked:
                        return self.askNextQuestion()

    def askNextQuestion(self):
        'Asks the next question'
        listDir = os.listdir(self.__quizzDir)
        if len(listDir) == len(self.__questionDone):
            del self.__questionDone[:]

        index = random.randint(0, len(listDir)-1)
        while index in self.__questionDone:
            index = random.randint(0, len(listDir)-1)

        with open(self.__quizzDir + "/" + listDir[index], "r") as f_question:
            self.__currentQuestion = f_question.readlines()

        self.__questionAsked = True
        self.__questionDone.append(index)
        return self.__currentQuestion[0]


    @botcmd
    def _quit(self, mess, args):
        """Logs out"""
        if str(mess.getFrom()).find(self.__admin_jid) == 0:
            self.quit()
            return "I quit!"
        else:
            usrnm = self.get_sender_username(mess)
        return str(usrnm)+ " : Not authorized!"


    @botcmd
    def _join(self, mess, args):
        """Joins a groupchat"""
        if str(mess.getFrom()).find(self.__admin_jid) == 0:
            if re.match('^(\w+)@(\w+)(\.(\w+))+$', args):
                self.join_room(args)
                self.__groupchat = args
                return "joined "+args
            else:
                return "Malformed url"
        else:
            usrnm = self.get_sender_username(mess)
        return str(usrnm)+ " : Not authorized!"

if __name__ == '__main__':
    #dirty fix, but needed to use unicode…
    reload(sys)
    sys.setdefaultencoding("utf-8")
    BOT = Quizzibal()
    BOT.serve_forever()
