#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'Quizzibal: a silly jabber quizz bot'
from jabberbot import JabberBot, botcmd
import xmpp
import datetime
import time
import re
import random
import os
import sys
import config


class Quizzibal(JabberBot):

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
        my_room_JID = "%s/%s" % (room,self.__nickname)
        self.connect().send(xmpp.Presence(to=my_room_JID))

    def unknown_command(self, mess, cmd, args):
        m = re.search("^("+self.__nickname+")(( )?(: |, )?)(start|stop|score|next)", mess.getBody())
        if m:
            return self.quizzHandler(m)
        else:
            m = re.search("^("+self.__nickname+")(( )?(: |, )?)((\w| |[éèçàêâûîôäëüïö'])+)", mess.getBody())
            if m:
                    #print m.groups()
                return self.quizzAnswerHandler(m, self.get_sender_username(mess))
            else:
                m = re.search("^question add$", mess.getBody())
                if m and mess.getType() == "chat" and self.__addingQuestion == False:
                    return self.questionAdder(mess, "prequestion")
                else:
                    if self.__addingQuestion == True  and mess.getType() == "chat":
                        return self.questionAdder(mess, "question")

    def questionAdder(self, message, state):
        if state == "prequestion":
            self.__addingQuestion = True
            text = "Enter your question, in a single message %s.\nDo not forget the template:\n" % (self.get_sender_username(message))
            text += "Question sur une seule ligne, sans faute d'orthographe si possible ?\nreponse possible (sur une seule ligne, la casse n'est pas prise en compte)\nautre reponse possible (par le bot, donc pas la peine de faire une ligne par)\nitou (variation possible de casse)\nde même\nditto\ntoujours pareil\netc\ntoossa"
            return text
        else:
            if state == "question":
                if self.__currentQuestionFileAdded == "":
                    self.__currentQuestionFileAdded = "%s/%s.%s.quizz" % (self.__quizzDir, self.get_sender_username(message), time.time())
                    fileOut = open(self.__currentQuestionFileAdded, 'a')
                    fileOut.write(message.getBody()+"\n")
                    fileOut.close()
                    self.__addingQuestion = False
                    self.__currentQuestionFileAdded = ""
                    return "Your question has been successfully added, " + self.get_sender_username(message)

    def quizzScoreHandler(self):
        str = ""
        for i in self.__score.keys():
            str += i +': %d\n' % (self.__score[i])
        return str

    def quizzAnswerHandler(self, matchobject, username):
        if self.__questionAsked:
            answer = matchobject.group(5)
            for i in range(1,len(self.__currentQuestion)):
                if re.match(answer, self.__currentQuestion[i], re.IGNORECASE):
                    if username in self.__score:
                        self.__score[username] += 1
                    else:
                        self.__score[username] = 1
                        
                    self.__questionAsked = False
                    str = "Good answer " + username + " !\nYou have now %s points" % (self.__score[username]) + "\nNext question: " + self.askNextQuestion()
                    return str            
            return "Sorry " + username + ", " + answer + " is not the answer to my question."
        else:
            return "Sorry, the answer to this question has already been given or there is no question running"

    def quizzHandler(self, matchobject):
        str = matchobject.group(5)
        if str == "start" and not self.__quizzMode:
            self.__quizzMode = True
            if self.__quizzMode and os.access(self.__quizzDir, os.F_OK) and not self.__questionAsked:
                return self.askNextQuestion()
            else:
                self.__quizzMode = False
                return "Quizz directory does not exist, cannot proceed"
        else:
            if str == "stop":
                self.__quizzMode = False     
                return "Quizz stopped"
            else:
                if str == "score":
                    return self.quizzScoreHandler()
                else:
                    if str == "next" and not self.__questionAsked:
                        return self.askNextQuestion()                     

    def askNextQuestion(self):
        listDir = os.listdir(self.__quizzDir)
        if len(listDir) == len(self.__questionDone):
            del self.__questionDone[:]
        #self.__currentFile = "%s" % (random.randint(1, len(os.listdir(self.__quizzDir))))
        numero = random.randint(0,len(listDir)-1)
        while numero in self.__questionDone:
            numero = random.randint(0,len(listDir)-1)
        fileIn = open(self.__quizzDir + "/" + listDir[numero], "r")
        self.__currentQuestion = fileIn.readlines()
        self.__questionAsked = True
        self.__questionDone.append(numero)
        return self.__currentQuestion[0]

    @botcmd
    def _quit (self, mess, args):
        """Logs out"""
        if str(mess.getFrom()).find(self.__admin_jid) == 0:
            self.quit()
            return "I quit!"
        else:
            usrnm = self.get_sender_username(mess)
        return str(usrnm)+ " : Not authorized!"

        
    @botcmd
    def _join (self, mess, args):
        """Joins a groupchat"""
        if str(mess.getFrom()).find(self.__admin_jid) == 0:
            if(re.match('^(\w+)@(\w+)(\.(\w+))+$', args)):
                self.join_room(args)
                self.__groupchat = args
                return "joined "+args
            else:
                return "Malformed url"
        else:
            usrnm = self.get_sender_username(mess)
        return str(usrnm)+ " : Not authorized!"

if __name__ ==  '__main__':
    bot = Quizzibal()

    #dirty fix, but needed to use unicode…
    reload(sys)
    sys.setdefaultencoding("utf-8")
    bot.serve_forever()
