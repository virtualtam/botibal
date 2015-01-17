# -*- coding: utf-8 -*-
'MiniBal: a minimalist jabber bot'
import datetime
import re
import sqlite3
from jabberbot import JabberBot, botcmd
import xmpp
from minibal.taunt import Tauntionary

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
        self.db_conn = sqlite3.connect('data.db')
        self.tauntionary = Tauntionary(self.db_conn)


    def join_groupchat(self, room):
        'Joins the specified multi-user chat room'
        room_jid = '{}/{}'.format(room, self.nickname)
        self.groupchat = room
        self.connect().send(xmpp.Presence(to=room_jid))


    @botcmd
    def _join(self, mess, args):
        'Joins a groupchat'
        if self.admin_jid in str(mess.getFrom()):
            if re.match(r'^(\w+)@(\w+)(\.(\w+))+$', args):
                self.join_groupchat(args)
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
            self.db_conn.close()
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
            return 'No groupchat joined'

        if name != self.nickname\
           or mess.getFrom().getResource() == self.nickname:
            return

        self.send(self.groupchat,
                  'plop {}'.format(mess.getFrom().getResource()),
                  None, 'groupchat')

    @botcmd
    def _taunt(self, mess, name):
        'Taunts someone'
        taunt = ''

        if name:
            taunt = '{}: '.format(name)

        try:
            taunt += self.tauntionary.taunt()
            return taunt
        except ValueError:
            return 'The tauntionary is empty'


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
