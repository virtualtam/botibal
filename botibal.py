#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'Botibal: a silly XMPP bot'
import codecs
import logging
import re
import sys

from minibal.client import MiniBal
from minibal.fukung import Fukung, REGEX
import config


class BotiBal(MiniBal):
    'A silly fukung-addict XMPP bot'
    # pylint: disable=too-many-public-methods

    def __init__(self, jid, password, nick, room, admin_jid):
        # pylint: disable=too-many-arguments
        super(BotiBal, self).__init__(jid, password, nick, room, admin_jid)
        self.fukung = Fukung(self.db_conn)

    def message(self, msg):
        if msg['mucnick'] == self.nick:
            return

        if msg['type'] not in ('chat', 'normal'):
            return

        super(BotiBal, self).message(msg)

        cmd, args = self.parse_user_command(msg)
        if cmd is None:
            return

        if cmd == 'fukung':
            try:
                self.say_group(self.fukung.get_link())
            except ValueError:
                msg.reply('no existing link').send()

        elif cmd == 'fukung_add':
            matches = re.search(REGEX, args)
            if matches:
                self.fukung.add_link_url(matches)

        elif cmd == 'fukung_list':
            msg.reply(str(self.fukung)).send()

        elif cmd == 'rot13':
            msg.reply(codecs.encode(args, 'rot_13')).send()

    def muc_message(self, msg):
        if msg['mucnick'] == self.nick:
            return

        super(BotiBal, self).muc_message(msg)

        # parse the messages to find fukung links
        matches = re.search(REGEX, msg['body'])
        if matches:
            self.fukung.add_link_url(matches)
            return

        cmd, args = self.parse_muc_command(msg)

        if cmd == 'fukung':
            try:
                self.say_group(self.fukung.get_link())
            except ValueError:
                self.say_group('the list is empty! plz browse dah internetz!')

        elif cmd == 'rot13':
            self.say_group(codecs.encode(args, 'rot_13'))


if __name__ == '__main__':
    if sys.version_info < (3, 0):
        from sleekxmpp.util.misc_ops import setdefaultencoding
        setdefaultencoding('utf8')

    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)-8s %(message)s')

    BOT = BotiBal(config.JID, config.PASSWORD, 'Botibal',
                  config.ROOM, config.ADMIN_JID)
    if BOT.connect():
        BOT.process(block=True)
    else:
        print 'Unable to connect'
