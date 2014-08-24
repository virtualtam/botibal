# -*- coding: utf-8 -*-
'MiniBal: a minimalist jabber bot'
from jabberbot import JabberBot, botcmd
import xmpp
import datetime
import re
import random

# pylint: disable=too-many-public-methods,unused-argument
class MiniBal(JabberBot):
    'Minimalist bot'
    def __init__(self, jid, password, nickname, admin_jid):
        self.jid = jid
        self.password = password
        self.nickname = nickname
        self.admin_jid = admin_jid
        self.groupchat = None
        super(MiniBal, self).__init__(self.jid, self.password)

        with open('insults.txt', 'r') as f_insults:
            self.insults = f_insults.readlines()


    def join_groupchat(self, room):
        'Joins the specified multi-user chat room'
        room_jid = '{}/{}'.format(room, self.nickname)
        self.connect().send(xmpp.Presence(to=room_jid))


    @botcmd
    def _join(self, mess, args):
        'Joins a groupchat'
        if self.admin_jid in str(mess.getFrom()):
            if re.match(r'^(\w+)@(\w+)(\.(\w+))+$', args):
                self.join_groupchat(args)
                self.groupchat = args
                return "joined "+args
            else:
                return "Malformed url"
        else:
            usrnm = self.get_sender_username(mess)
        return str(usrnm)+ " : Not authorized!"


    @botcmd
    def _quit(self, mess, args):
        'Logs out'
        if self.admin_jid in str(mess.getFrom()):
            self.quit()
            return "I quit!"
        else:
            usrnm = self.get_sender_username(mess)
        return str(usrnm)+ ": Not authorized!"


    @botcmd
    def _say(self, mess, args):
        'Says something'
        usrnm = self.get_sender_username(mess)
        if re.match('^_(.)*', args):
            return 'Do not try to unleash the infinite fury, {}'.format(
                str(usrnm))
        else:
            return args


    @botcmd
    def _sayg(self, mess, args):
        'Sends a message to the current groupchat'
        self.send(self.groupchat, self._say(mess, args), None, 'groupchat')


    @botcmd
    def plop(self, mess, name):
        '''Cordially answers a user's plopping'''
        if self.groupchat is None:
            return

        if name is not self.nickname\
           or mess.getFrom().getResource() is self.nickname:
            return

        self.send(self.groupchat,
                  'plop {}'.format(mess.getFrom().getResource()),
                  None, 'groupchat')

    @botcmd
    def _insult(self, mess, name):
        'Insults someone'
        insult = ''

        if name:
            insult = '{} : '.format(name)

        insult += self.insults[random.randint(0, len(self.insults))]
        return insult.replace('\n', '')


    @botcmd
    def _whoami(self, mess, args):
        """Tells you your username"""
        usrnm = self.get_sender_username(mess)
        return str(usrnm)+": You are "+str(mess.getFrom())+"..."

    @botcmd
    def _time(self, mess, args):
        'Displays the current server time'
        usrnm = self.get_sender_username(mess)
        return str(usrnm)+" : "+str(datetime.datetime.today())
