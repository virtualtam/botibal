#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'Botibal: a silly jabber bot'
from jabberbot import JabberBot, botcmd
import xmpp
import datetime
import re
import random
import os
import sys
import fileinput
import config


class Botibal(JabberBot):

    __jid = config.JID
    __password = config.PASSWORD
    __admin = config.ADMIN_JID

    __groupchat = None
    __nickname = config.NICK

    __fukung = 'http://(www\.)?fukung.net/v/(\d+)/(\w+)\.(\w+)'

    __fails = dict()


    def __init__(self):
        super(Botibal, self).__init__(self.__jid, self.__password)

    def join_room(self, room):
        """Join the specified multi-user chat room"""
        my_room_JID = "%s/%s" % (room,self.__nickname)
        self.connect().send(xmpp.Presence(to=my_room_JID))

    def unknown_command(self, mess, cmd, args):
        if self.get_sender_username(mess) != self.__nickname:
            m = re.search(self.__fukung, mess.getBody())
            if m:
                self.appendToFukung(m)
                return
            else:
                return self.failsHandler(mess)

    def failsHandler(self, mess):
        m = re.search('('+self.__nickname+': )?fails add (\w+)', mess.getBody())
        if m:
            return self.failcount('add', m.group(2))
        else:
            m = re.search('('+self.__nickname+': )?fails( dump)? ?(\w+@\w+\.\w+)?', mess.getBody())
            if m:
                if m.group(3):
                    if m.group(2):
                        return self.failcount(m.group(2), m.group(3))
                    else:
                        return self.failcount('dump', m.group(3))
                else:
                    if m.group(2):
                        return self.failcount(m.group(2), 'all')
 #                   else:
#                        return self.failcount('dump', 'all')
            else:
                m = re.search('('+self.__nickname+'(:|,)? )(failcount|fails|fail)\+\+', mess.getBody())
                if m:
                    return self.failcount('add', self.get_sender_username(mess))
                else:
                    m = re.search('('+self.__nickname+'(:|,)? )(failcount|fails|fail)--', mess.getBody())
                    if m:
                        return self.failcount('del', self.get_sender_username(mess))
                    else:
                        return None


    def appendToFukung(self, matchobject):
        fileOut = open('fukung.log', 'a')
        text = matchobject.group(2)+'/'+matchobject.group(3)+'.'+matchobject.group(4)+'\n'
        fileOut.write(text)
        fileOut.close()

    def readFukung(self, method = 'rand'):
        fileIn = open('fukung.log', 'r')
        lines = fileIn.readlines()
        if method == 'dump':
            str = ''
            for i in lines:
                str += 'http://www.fukung.net/v/'+i
            return str
        else:
            return 'http://www.fukung.net/v/'+lines[random.randint(0,len(lines))]

    def failcount(self, method, user):
        if method == 'dump' and self.__fails != None:
            if user == 'all':
                str = 'Fails: \n'
                for i in self.__fails.keys():
                    str += i +': %d\n' % (self.__fails[i])
                return str
            else:
                str = user +'\'s failcount: %d' % (self.__fails[user])
                if self.__fails[user] >= 5:
                    str += ' \n'+user+' shall now use a new name'
                return str
        else:
            if method == 'add' and user != 'all':
                if user in self.__fails:
                    self.__fails[user] += 1
                    return self.failcount('dump', user)
                else:
                    self.__fails[user] = 1
                    return self.failcount('dump', user)
            else:
                if method == 'del' and user != 'all':
                    if user in self.__fails and self.__fails[user] >= 1:
                        self.__fails[user] -= 1
                        return self.failcount('dump', user)
                    else:
                        return 'Error: failcount < 0 or unknown user'
                else:
                    return None

    @botcmd
    def fails(self, mess, args):
        """Displays fails"""
        usrnm = self.get_sender_username(mess)
        if(re.match('^_(.)*', args)):
            return "Do not try to unleash the infinite fury, "+str(usrnm)
        else:
            return self.failcount('dump', 'all')

    @botcmd
    def _time( self, mess, args):
        """Displays current server time"""
        usrnm = self.get_sender_username(mess)
        return str(usrnm)+" : "+str(datetime.datetime.today())

    @botcmd
    def _rot13( self, mess, args):
        """Returns passed arguments rot13'ed"""
        usrnm = self.get_sender_username(mess)
        return str(usrnm)+" : "+args.encode('rot13')

    @botcmd
    def _whoami( self, mess, args):
        """Tells you your username"""
        usrnm = self.get_sender_username(mess)
        return str(usrnm)+": You are "+str(mess.getFrom())+"..."

    @botcmd
    def _quit (self, mess, args):
        """Logs out"""
        if str(mess.getFrom()).find(""+self.__admin+"") == 0:
            self.quit()
            return "I quit!"
        else:
            usrnm = self.get_sender_username(mess)
        return str(usrnm)+ " : Not authorized!"


    @botcmd
    def _join (self, mess, args):
        """Joins a groupchat"""
        if str(mess.getFrom()).find(""+self.__admin+"") == 0:
            if(re.match('^(\w+)@(\w+)(\.(\w+))+$', args)):
                self.join_room(args)
                self.__groupchat = args
                return "joined "+args
            else:
                return "Malformed url"
        else:
            usrnm = self.get_sender_username(mess)
        return str(usrnm)+ " : Not authorized!"

    @botcmd
    def _say(self, mess, args):
        """Says passed argument"""
        usrnm = self.get_sender_username(mess)
        if(re.match('^_(.)*', args)):
            return "Do not try to unleash the infinite fury, "+str(usrnm)
        else:
            return args

    @botcmd
    def _sayg(self, mess, args):
        """Sends a message to currently joined groupchat"""
        self.send(self.__groupchat, self._say(mess, args), None, 'groupchat')

    @botcmd
    def plop(self, mess, name):
        """Responds to a plopping"""
        if self.__groupchat != None :
            if name==self.__nickname and mess.getFrom().getResource() != self.__nickname :
                self.send(self.__groupchat, 'plop '+mess.getFrom().getResource(), None, 'groupchat')
                return
        else:
            return

    @botcmd
    def _fshow(self, mess, args):
        """Gives an almost random image url from fukung"""
        if args == 'dump':
            return self.readFukung(method=args)
        else:
            return self.readFukung()

    @botcmd
    def _insult(self, mess, name):
        """Insults someone"""
        fileIn = open('insults.txt', 'r')
        lines = fileIn.readlines()
        if name:
            ret = name + ' : '
        else:
            ret = ''
        ret = ret + lines[random.randint(0,len(lines))].replace('\n', '')
        fileIn.close()
        return ret

if __name__ == '__main__':
    #dirty fix, but needed to use unicode…
    reload(sys)
    sys.setdefaultencoding("utf-8")
    bot = Botibal()
    bot.serve_forever()
