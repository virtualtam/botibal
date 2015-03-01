# -*- coding: utf-8 -*-
'botibal.client.minibal unit tests'
# pylint: disable=too-many-public-methods
import unittest

from sleekxmpp.stanza import Message

from botibal.client.cmd_parser import PrivilegeError
from botibal.client.minibal import MiniBal, TAUNT_LEN_MAX

from tests.client.utils import MockMiniBal, ClientTestCase


class TestMiniBal(ClientTestCase):
    'Covers command parsing'
    def setUp(self):
        super(TestMiniBal, self).setUp()
        self.client = MockMiniBal('bot@server.org', 'p455w0rd', 'bot',
                                  'room@server.org', 'admin@server.org',
                                  self.test_db)

    def test_init(self):
        'Build-Bot :-)'
        MiniBal('bot@server.org', 'p455w0rd', 'bot',
                'room@server.org', 'admin@server.org', self.test_db)

    def test_pm_say(self):
        'Say something (from PM)'
        args = self._parse_cmd('say toto')
        args.func(None, args)
        self.assertSayGroupEqual('toto')

    def test_muc_say(self):
        'Say something (from MUC)'
        args = self._parse_muc_cmd('say toto')
        args.func(None, args)
        self.assertSayGroupEqual('toto')

    def test_say_infinite(self):
        "Attempt to use the bot's name"
        msg = Message()
        cmd = 'say {}'.format(self.client.nick)

        args = self._parse_cmd(cmd)
        args.func(msg, args)
        self.assertEqual(self.client.reply,
                         'Do not try to unleash the infinite fury, ')

        args = self._parse_muc_cmd(cmd)
        args.func(msg, args)
        self.assertEqual(self.client.reply,
                         'Do not try to unleash the infinite fury, ')

    def test_date(self):
        'Tick, tock'
        self.client.date(None, self._parse_cmd('date'))
        self.client.date(None, self._parse_cmd('date -i'))
        self.client.date(None, self._parse_cmd('date -r'))
        self.client.date(None, self._parse_cmd('date -f %Y %m %d'))

    def test_quit_user(self):
        'A non-admin user attempts to stop the bot'
        with self.assertRaises(PrivilegeError):
            self.client.quit(Message(), None)

    def test_quit_custom_message(self):
        'Disconnect with a custom message'
        self.client.quit(Message(sfrom='admin@server.org'),
                         self._parse_cmd('quit good night!'))
        self.assertSayGroupEqual('good night!')

    def test_quit(self):
        'Disconnect with a custom message'
        self.client.quit(Message(sfrom='admin@server.org'),
                         self._parse_cmd('quit'))
        self.assertSayGroupEqual('I quit!')

    def test_muc_empty_taunt(self):
        'Taunt someone from the MUC (empty tauntionary)'
        self.client.taunt(None, self._parse_cmd('taunt'))
        self.assertReplyEqual('The tauntionary is empty')
        self.assertSayGroupEqual('')
        self.client.taunt(None, self._parse_cmd('taunt Hans'))
        self.assertReplyEqual('The tauntionary is empty')
        self.assertSayGroupEqual('')

    def test_muc_taunt_index(self):
        'Taunt s/o, with a selected piece'
        self.client.tauntionary.add_taunt('blorgh!', 'Igor')
        self.client.taunt(None, self._parse_cmd('taunt Hans -n 1'))
        self.assertSayGroupEqual('Hans: blorgh!')

    def test_muc_taunt_index_error(self):
        'Taunt s/o, with a selected piece: IndexError Deluxe Edition'
        self.client.tauntionary.add_taunt('blorgh!', 'Igor')
        self.client.taunt(None, self._parse_cmd('taunt Hans -n 86'))
        self.assertReplyEqual("taunt #86 doesn't exist")
        self.assertSayGroupEqual('')

    def test_muc_taunt(self):
        'Taunt someone from the MUC'
        self.client.tauntionary.add_taunt('blorgh!', 'Igor')

        self.client.taunt(None, self._parse_muc_cmd('taunt'))
        self.assertSayGroupEqual('blorgh!')
        self.client.taunt(None, self._parse_muc_cmd('taunt Grichka'))
        self.assertSayGroupEqual('Grichka: blorgh!')

    def test_taunt_nick_with_spaces(self):
        'Taunt someone from the MUC, whose nick contains spaces'
        self.client.tauntionary.add_taunt('blorgh!', 'Igor')

        self.client.taunt(None, self._parse_muc_cmd('taunt'))
        self.assertSayGroupEqual('blorgh!')
        self.client.taunt(None, self._parse_muc_cmd('taunt Grich Ka'))
        self.assertSayGroupEqual('Grich Ka: blorgh!')

    def test_add_too_long_taunt(self):
        'Attempt to add a taunt that exceeds the max authorized length'
        tnt = ''.join(['a'] * TAUNT_LEN_MAX)

        self.client.taunt(Message(),
                          self._parse_cmd('taunt -a long{}'.format(tnt)))
        self.assertEqual(self.client.reply,
                         'too long a taunt, sir!')

    def test_add_invalid_taunt(self):
        'Add an invalid taunt'
        self.client.taunt(Message(),
                          self._parse_cmd('taunt -a blorgh!'))
        self.assertEqual(self.client.reply,
                         'error: Taunt: empty user nickname')

    def test_list_empty_taunt(self):
        'Ask for the (empty) list of taunts'
        self.client.taunt(Message(), self._parse_cmd('taunt -l'))
        self.assertEqual(self.client.reply, '\n')


if __name__ == '__main__':
    unittest.main()
