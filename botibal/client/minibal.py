# -*- coding: utf-8 -*-
"""
MiniBal: a minimalist jabber bot

Contains the core structure for XMPP bot-i-bals:
- common features,
- command parsing and handling,
- overridable hooks.

The command parser extensively uses Argparse and subcommands;
to add new features/ commands, the following methods can be overriden:
- add_common_commands           common commands,
- add_message_commands          PM (admin) commands,
- add_muc_commands              MUC commands,
- muc_hook                      pre-command-parsing MUC hook.
"""
import datetime
import re
import sqlite3

from sleekxmpp import ClientXMPP

from botibal.client.cmd_parser import BotCmdParser, BotCmdError, PrivilegeError
from botibal.taunt import Tauntionary


class MiniBal(ClientXMPP):
    'A minimalist XMPP bot'
    # pylint: disable=too-many-public-methods

    def __init__(self, jid, password, nick, room, admin_jid):
        # pylint: disable=too-many-arguments
        super(MiniBal, self).__init__(jid, password)
        self.room = room
        self.nick = nick
        self.admin_jid = admin_jid

        self.cmd_parser = BotCmdParser(prog='{}: '.format(self.nick))
        self.muc_cmd_parser = BotCmdParser(prog='{}: '.format(self.nick))
        self.setup_command_parsers()

        self.add_event_handler('session_start', self.session_start)
        self.add_event_handler('message', self.message)
        self.add_event_handler('groupchat_message', self.muc_message)

        self.register_plugin('xep_0030')  # Service Discovery
        self.register_plugin('xep_0045')  # Multi-User Chat
        self.register_plugin('xep_0199')  # XMPP Ping

        self.db_conn = sqlite3.connect('data.db', check_same_thread=False)
        self.tauntionary = Tauntionary(self.db_conn)

    def session_start(self, event):
        'Starts an XMPP session and connects to a MUC'
        # pylint: disable=unused-argument
        self.send_presence()
        self.get_roster()
        self.plugin['xep_0045'].joinMUC(self.room, self.nick, wait=True)

    def message(self, msg):
        """
        Handles PM messages and maps them to user commands
        """
        if msg['mucnick'] == self.nick:
            return
        if msg['type'] not in ('chat', 'normal'):
            return

        try:
            args = self.cmd_parser.parse_args(msg['body'].split(' '))
        except BotCmdError, err:
            msg.reply('\n{}'.format(err)).send()
            return

        try:
            args.func(msg, args)
        except PrivilegeError, err:
            msg.reply(str(err)).send()

    def muc_hook(self, msg):
        'MUC hook executed before parsing commands'
        if msg['body'] == 'plop {}'.format(self.nick):
            self.say_group('plop {}'.format(msg['mucnick']))
            return True

    def muc_message(self, msg):
        """
        Handles MUC messages and maps them to user commands
        """
        if msg['mucnick'] == self.nick:
            return

        if self.muc_hook(msg) is True:
            return

        if not msg['body'].startswith(self.nick):
            return

        cmdline = re.sub(r'{}[ ]?[,:]? '.format(self.nick), '',
                         msg['body'])

        try:
            args = self.muc_cmd_parser.parse_args(cmdline.split(' '))
        except BotCmdError, err:
            self.say_group('\n{}'.format(err))
            return

        args.func(msg, args)

    def quit(self, msg, args):
        'Logs out'
        if msg['from'].bare != self.admin_jid:
            raise PrivilegeError('nah. admin only!')

        if args.text is not None and args.text != []:
            self.say_group(' '.join(args.text))
        else:
            self.say_group('I quit!')

        self.disconnect(wait=5.0, send_close=True)

    def say(self, msg, args):
        'Says something'
        if self.nick in args.text:
            msg.reply('Do not try to unleash the infinite fury, {}'.format(
                msg['mucnick'])).send()
            return

        self.say_group(' '.join(args.text))

    def say_group(self, text):
        'Sends a message to the MUC'
        self.send_message(mto=self.room, mbody=text, mtype='groupchat')

    def time(self, msg, args):
        'Tick, tock'
        # pylint: disable=unused-argument
        # TODO: customize output formatting
        self.say_group(str(datetime.datetime.today()))

    def taunt(self, msg, args):
        'Controls taunt interactions'
        # pylint: disable=unused-argument
        try:
            # message parser
            if args.list:
                msg.reply('\n{}'.format(self.tauntionary)).send()
                return

            elif args.add:
                try:
                    self.tauntionary.add_taunt(' '.join(args.add),
                                               msg['from'].resource)
                except ValueError, err:
                    msg.reply('error: {}'.format(err)).send()
                return
        except AttributeError:
            # MUC parser
            pass

        taunt = ''

        if args.nick is not None:
            taunt = '{}: '.format(args.nick)

        try:
            taunt += self.tauntionary.taunt()
            self.say_group(taunt)
        except ValueError:
            self.say_group('The tauntionary is empty')

    def add_common_commands(self, subparser):
        'Adds common message / MUC commands to a subparser'
        p_say = subparser.add_parser('say', help='say something')
        p_say.add_argument('text', type=str, nargs='+')
        p_say.set_defaults(func=self.say)

        p_time = subparser.add_parser('time', help='')
        p_time.set_defaults(func=self.time)

    def add_message_commands(self, subparser):
        'Adds message commands to a subparser'
        p_quit = subparser.add_parser('quit', help='tells the bot to stop')
        p_quit.add_argument('text', type=str, nargs='*')
        p_quit.set_defaults(func=self.quit)

        p_taunt = subparser.add_parser('taunt', help='manage taunts')
        p_taunt.add_argument('nick', type=str, nargs='?')
        p_taunt.add_argument('-a', '--add', type=str, nargs='+',
                             help='add a new taunt')
        p_taunt.add_argument('-l', '--list', help='list taunts',
                             action='store_true')
        p_taunt.set_defaults(func=self.taunt)

    def add_muc_commands(self, subparser):
        'Adds message commands to a subparser'
        p_taunt = subparser.add_parser('taunt', help='taunt someone')
        p_taunt.add_argument('nick', type=str, nargs='?')
        p_taunt.set_defaults(func=self.taunt)

    def setup_command_parsers(self):
        'Setups message and MUC command parsers'
        # message (PM) commands
        msg_sub = self.cmd_parser.add_subparsers()
        self.add_common_commands(msg_sub)
        self.add_message_commands(msg_sub)

        # groupchat (MUC) commands
        muc_sub = self.muc_cmd_parser.add_subparsers()
        self.add_common_commands(muc_sub)
        self.add_muc_commands(muc_sub)
