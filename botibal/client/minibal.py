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
import re
import sqlite3
from datetime import datetime, timedelta
from email.utils import formatdate

from slixmpp import ClientXMPP

from botibal.client.cmd_parser import (BotCmdError, BotCmdParser, BotHelp,
                                       PrivilegeError)
from botibal.taunt import Tauntionary


TAUNT_LEN_MAX = 197  # 197 (10) is 101 (14), which is kinda cool, huh?


class MiniBal(ClientXMPP):
    """
    A minimalist XMPP bot
    """

    # pylint: disable=too-many-public-methods,too-many-instance-attributes

    def __init__(self, jid, password, nick, room, admin_jid,
                 database='data.db'):
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

        self.db_conn = sqlite3.connect(database, check_same_thread=False)
        self.tauntionary = Tauntionary(self.db_conn)
        self.plops = dict()

    def session_start(self, event):
        """
        Starts an XMPP session and connects to a MUC
        """
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
        except BotCmdError as err:
            self.send_reply(msg, '\n{}'.format(err))
            return

        try:
            args.func(msg, args)
        except PrivilegeError as err:
            self.send_reply(msg, str(err))

    def muc_hook(self, msg):
        """
        MUC hook executed before parsing commands
        """
        if self.plop(msg):
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
        except BotHelp as err:
            self.say_group('\n{}'.format(err))
            return
        except BotCmdError:
            return

        args.func(msg, args)

    def quit(self, msg, args):
        """
        Logs out
        """
        if msg['from'].bare != self.admin_jid:
            raise PrivilegeError('nah. admin only!')

        if args.text is not None and args.text != []:
            self.say_group(' '.join(args.text))
        else:
            self.say_group('I quit!')

        self.disconnect(wait=5.0)

    def send_reply(self, msg, text):
        """
        Replies to a private message
        """
        # pylint: disable=no-self-use
        msg.reply(text).send()

    def say(self, msg, args):
        """
        Says something
        """
        if self.nick in args.text:
            self.send_reply(
                msg,
                'Do not try to unleash the infinite fury, {}'
                .format(msg['mucnick']))
            return

        self.say_group(' '.join(args.text))

    def say_group(self, text):
        """
        Sends a message to the MUC
        """
        self.send_message(mto=self.room, mbody=text, mtype='groupchat')

    def date(self, _, args):
        """
        Tick, tock
        """
        curdate = datetime.today()

        if args.format:
            # custom format
            date_str = curdate.strftime(' '.join(args.format))

        elif args.iso:
            # ISO 8601 (default format)
            # 2015-02-24 23:23:42.823837
            date_str = curdate.isoformat(' ')
        elif args.rfc2822:
            # RFC 2822
            # Tue, 24 Feb 2015 22:23:27 -0000
            date_str = formatdate()
        else:
            # 2015-02-24 23:23:47.641520
            date_str = str(curdate)

        self.say_group(date_str)

    def plop(self, msg):
        """
        For those about to plop

            We salute you!
        """
        matches = re.match(
            r'^(\w+) {nick}([ ]?[!]?)'.format(nick=self.nick),
            msg['body'],
            re.UNICODE
        )

        if matches is None:
            return False

        now = datetime.now()

        if (msg['mucnick'] in self.plops.keys() and
                now - self.plops[msg['mucnick']] < timedelta(days=1)):
            # the plopping courtesy is to happen at most once a day
            self.say_group('meh.')
            return True

        self.plops[msg['mucnick']] = now
        self.say_group(
            '{} {}{}'.format(
                matches.group(1),
                msg['mucnick'],
                matches.group(2)
            )
        )
        return True

    def taunt(self, msg, args):
        """
        Controls taunt interactions
        """
        if args.lg:
            self.send_reply(msg, '\n{}'.format(
                self.tauntionary.list_by_aggro()))

        elif args.list:
            self.send_reply(msg, '\n{}'.format(self.tauntionary))

        elif args.add:
            if len(''.join(args.add)) > TAUNT_LEN_MAX:
                self.send_reply(msg, 'too long a taunt, sir!')
                return

            try:
                self.tauntionary.add_taunt(' '.join(args.add),
                                           msg['from'].resource,
                                           args.aggro)
            except ValueError as err:
                self.send_reply(msg, 'error: {}'.format(err))

        elif args.aggro:
            if not args.number:
                self.send_reply(msg, 'no taunt specified')
                return

            self.tauntionary.set_aggro(args.number, args.aggro)

        else:
            taunt = ''

            if args.nick is not None and args.nick != []:
                taunt = '{}: '.format(' '.join(args.nick))

            try:
                try:
                    taunt += self.tauntionary.taunt(args.number)
                except IndexError:
                    self.send_reply(
                        msg, "taunt #{} doesn't exist".format(args.number))
                    return
                except AttributeError:
                    taunt += self.tauntionary.taunt()

                self.say_group(taunt)

            except ValueError:
                self.send_reply(msg, 'The tauntionary is empty')

    def add_common_commands(self, subparser):
        """
        Adds common message / MUC commands to a subparser
        """
        p_say = subparser.add_parser('say', help='say something')
        p_say.add_argument('text', type=str, nargs='+')
        p_say.set_defaults(func=self.say)

        p_date = subparser.add_parser('date',
                                      help='gives the current date and time')
        p_date.add_argument('-f', '--format', type=str, nargs='+',
                            help='custom format, e.g. %%Y %%m %%d')
        p_date.add_argument('-i', '--iso', action='store_true',
                            help='ISO 8601 format (default)')
        p_date.add_argument('-r', '--rfc2822', action='store_true',
                            help='RFC 2822 format')
        p_date.set_defaults(func=self.date)

    def add_message_commands(self, subparser):
        """
        Adds message commands to a subparser
        """
        p_quit = subparser.add_parser('quit', help='tells the bot to stop')
        p_quit.add_argument('text', type=str, nargs='*')
        p_quit.set_defaults(func=self.quit)

        p_taunt = subparser.add_parser('taunt', help='manage taunts')
        p_taunt.add_argument('nick', type=str, nargs='*')
        p_taunt.add_argument('-a', '--add', type=str, nargs='+',
                             help='add a new taunt')
        p_taunt.add_argument('-g', '--aggro', type=int,
                             help='define the aggro level of a taunt')
        p_taunt.add_argument('-l', '--list', help='list taunts',
                             action='store_true')
        p_taunt.add_argument('-L', '--lg', help='list taunts by aggro level',
                             action='store_true')
        p_taunt.add_argument('-n', '--number', type=int,
                             help='select a taunt')
        p_taunt.set_defaults(func=self.taunt)

    def add_muc_commands(self, subparser):
        """
        Adds groupchat commands to a subparser
        """
        pass

    def setup_command_parsers(self):
        """
        Setups message and MUC command parsers
        """
        # message (PM) commands
        msg_sub = self.cmd_parser.add_subparsers()
        self.add_common_commands(msg_sub)
        self.add_message_commands(msg_sub)

        # groupchat (MUC) commands
        muc_sub = self.muc_cmd_parser.add_subparsers()
        self.add_common_commands(muc_sub)
        self.add_muc_commands(muc_sub)
