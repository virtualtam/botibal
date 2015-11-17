# -*- coding: utf-8 -*-
"""
Botibal: a silly XMPP bot
"""
import codecs

from botibal.client.minibal import MiniBal
from botibal.fukung import Fukung


class BotiBal(MiniBal):
    """
    A silly fukung-addict XMPP bot
    """

    # pylint: disable=too-many-public-methods

    def __init__(self, jid, password, nick, room, admin_jid,
                 database='data.db'):
        # pylint: disable=too-many-arguments
        super(BotiBal, self).__init__(
            jid, password, nick, room, admin_jid, database)
        self.fukung = Fukung(self.db_conn)

    def fukung_net(self, msg, args):
        """
        Controls Fukung interactions
        """
        try:
            # message parser
            if args.add:
                try:
                    self.fukung.add_link_url(args.add)
                except ValueError as err:
                    self.send_reply(msg, 'error: {}'.format(err))
                return

            elif args.list:
                self.send_reply(msg, '\n{}'.format(self.fukung))
                return
        except AttributeError:
            # MUC parser
            pass

        try:
            self.say_group(self.fukung.get_link())
        except ValueError:
            self.say_group('da fukung list iz empty! plz browse da intarnetz!')

    def rot13(self, _, args):
        """
        Applies rot13 on the passed string
        """
        self.say_group(codecs.encode(' '.join(args.text), 'rot_13'))

    def add_common_commands(self, subparser):
        super(BotiBal, self).add_common_commands(subparser)

        p_rot13 = subparser.add_parser('rot13', help="returns a rot13'd string")
        p_rot13.add_argument('text', type=str, nargs='+')
        p_rot13.set_defaults(func=self.rot13)

    def add_message_commands(self, subparser):
        super(BotiBal, self).add_message_commands(subparser)

        p_fukung = subparser.add_parser('fukung', help='manage Fukung links')
        p_fukung.add_argument('-a', '--add', type=str,
                              help='add a fukung link')
        p_fukung.add_argument('-l', '--list', action='store_true',
                              help='lists fukung links')
        p_fukung.set_defaults(func=self.fukung_net)

    def add_muc_commands(self, subparser):
        super(BotiBal, self).add_muc_commands(subparser)

        p_fukung = subparser.add_parser('fukung', help='manage Fukung links')
        p_fukung.set_defaults(func=self.fukung_net)

    def muc_hook(self, msg):
        super(BotiBal, self).muc_hook(msg)

        # parse the messages to find fukung links
        try:
            self.fukung.add_link_url(msg['body'])
        except ValueError:
            # don't print anything!
            # users are entitled to post the same link twice, thrice...
            pass
        return False
