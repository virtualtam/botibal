# -*- coding: utf-8 -*-
'MiniBal: a minimalist jabber bot'
import datetime
import re
import sqlite3

from sleekxmpp import ClientXMPP

from botibal.taunt import Tauntionary

class MiniBal(ClientXMPP):
    'Minimalist XMPP bot'
    # pylint: disable=too-many-public-methods

    def __init__(self, jid, password, nick, room, admin_jid):
        # pylint: disable=too-many-arguments
        super(MiniBal, self).__init__(jid, password)
        self.room = room
        self.nick = nick
        self.admin_jid = admin_jid

        self.cmd_regex = r'(\w+)[ ]?(.+)?'
        self.muc_cmd_regex = r'{}[ ]?[,:]? (\w+)[ ]?(.+)?'

        self.add_event_handler('session_start', self.session_start)
        self.add_event_handler('message', self.message)
        self.add_event_handler('groupchat_message', self.muc_message)

        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0045') # Multi-User Chat
        self.register_plugin('xep_0199') # XMPP Ping

        self.db_conn = sqlite3.connect('data.db', check_same_thread=False)
        self.tauntionary = Tauntionary(self.db_conn)

    def session_start(self, event):
        'Starts an XMPP session and connect to a MUC'
        # pylint: disable=unused-argument
        self.send_presence()
        self.get_roster()
        self.plugin['xep_0045'].joinMUC(self.room, self.nick, wait=True)

    def parse_user_command(self, msg):
        'Maps a user message to a command-arguments tuple'
        matches = re.match(self.cmd_regex, msg['body'])
        if matches is None:
            return (None, None)
        return (matches.group(1), matches.group(2))

    def parse_muc_command(self, msg):
        'Maps a MUC message to a command-arguments tuple'
        matches = re.match(self.muc_cmd_regex.format(self.nick), msg['body'])
        if matches is None:
            return (None, None)
        return (matches.group(1), matches.group(2))

    def message(self, msg):
        """
        Handles chat messages and maps them to:
        - user commands (from any user),
        - admin commands (from the admin jid).
        """
        if msg['mucnick'] == self.nick:
            return
        if msg['type'] not in ('chat', 'normal'):
            return

        cmd, args = self.parse_user_command(msg)
        if cmd is None:
            return

        # user commands
        if cmd == 'say':
            self.say_group(self.say(args, msg['from'].resource))
        elif cmd == 'taunt':
            self.taunt(args)
        elif cmd == 'taunt_add':
            self.tauntionary.add_taunt(args, msg['from'].resource)
        elif cmd == 'taunt_list':
            msg.reply(str(self.tauntionary)).send()

        if msg['from'].bare != self.admin_jid:
            return

        # admin commands
        if cmd == 'quit':
            msg.reply('I quit!').send()
            self.quit()

    def muc_message(self, msg):
        """
        Handles MUC messages and maps them to user commands
        """
        if msg['mucnick'] == self.nick:
            return

        if msg['body'] == 'plop {}'.format(self.nick):
            self.say_group('plop {}'.format(msg['mucnick']))
            return

        cmd, args = self.parse_muc_command(msg)
        if cmd is None:
            return

        if cmd == 'say':
            self.say_group(self.say(args, msg['mucnick']))
        elif cmd == 'taunt':
            self.taunt(args)
        elif cmd == 'time':
            self.say_group(str(datetime.datetime.today()))

    def quit(self):
        'Logs out'
        self.say_group('I quit!')
        self.disconnect(wait=5.0, send_close=True)

    def say(self, msg, mucnick):
        'Says something'
        if self.nick in msg:
            return 'Do not try to unleash the infinite fury, {}'.format(mucnick)

        if msg is None:
            return 'whatever...'

        return msg

    def say_group(self, msg):
        'Sends a message to the MUC'
        self.send_message(mto=self.room, mbody=msg, mtype='groupchat')

    def taunt(self, nick):
        'Taunts someone'
        taunt = ''

        if nick is not None:
            taunt = '{}: '.format(nick)

        try:
            taunt += self.tauntionary.taunt()
            self.say_group(taunt)
        except ValueError:
            self.say_group('The tauntionary is empty')
