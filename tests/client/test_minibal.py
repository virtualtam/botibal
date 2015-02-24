# -*- coding: utf-8 -*-
'botibal.client.minibal unit tests'
# pylint: disable=too-many-public-methods
from sleekxmpp.stanza import Message
import unittest

from botibal.client.cmd_parser import PrivilegeError
from botibal.client.minibal import MiniBal

from tests.utils import DBTestCase


class MockMiniBal(MiniBal):
    'Mock client for local testing'
    reply = ''
    text = ''

    def say_group(self, text):
        self.text = text

    def send_reply(self, msg, text):
        self.reply = text

    def disconnect(self, reconnect=False, wait=None, send_close=True):
        pass


class TestMiniBal(DBTestCase):
    'Covers command parsing'
    def setUp(self):
        super(TestMiniBal, self).setUp()
        self.minibal = MockMiniBal('bot@server.org', 'p455w0rd', 'bot',
                                   'room@server.org', 'admin@server.org',
                                   self.test_db)

    def _parse_cmd(self, cmd):
        'Parse a PM command'
        return self.minibal.cmd_parser.parse_args(cmd.split(' '))

    def _parse_muc_cmd(self, cmd):
        'Parse a PM command'
        return self.minibal.muc_cmd_parser.parse_args(cmd.split(' '))

    def test_init(self):
        'Build-Bot :-)'
        MiniBal('bot@server.org', 'p455w0rd', 'bot',
                'room@server.org', 'admin@server.org', self.test_db)

    def test_pm_say(self):
        'Say something (from PM)'
        args = self._parse_cmd('say toto')
        args.func(None, args)
        self.assertEqual(self.minibal.text, 'toto')

    def test_muc_say(self):
        'Say something (from MUC)'
        args = self._parse_muc_cmd('say toto')
        args.func(None, args)
        self.assertEqual(self.minibal.text, 'toto')

    def test_say_infinite(self):
        "Attempt to use the bot's name"
        msg = Message()
        cmd = 'say {}'.format(self.minibal.nick)

        args = self._parse_cmd(cmd)
        args.func(msg, args)
        self.assertEqual(self.minibal.reply,
                         'Do not try to unleash the infinite fury, ')

        args = self._parse_muc_cmd(cmd)
        args.func(msg, args)
        self.assertEqual(self.minibal.reply,
                         'Do not try to unleash the infinite fury, ')

    def test_date(self):
        'Tick, tock'
        self.minibal.date(None, self._parse_cmd('date'))
        self.minibal.date(None, self._parse_cmd('date -i'))
        self.minibal.date(None, self._parse_cmd('date -r'))
        self.minibal.date(None, self._parse_cmd('date -f %Y %m %d'))

    def test_quit_user(self):
        'A non-admin user attempts to stop the bot'
        with self.assertRaises(PrivilegeError):
            self.minibal.quit(Message(), None)

    def test_quit_custom_message(self):
        'Disconnect with a custom message'
        self.minibal.quit(Message(sfrom='admin@server.org'),
                          self._parse_cmd('quit good night!'))
        self.assertEqual(self.minibal.text, 'good night!')

    def test_quit(self):
        'Disconnect with a custom message'
        self.minibal.quit(Message(sfrom='admin@server.org'),
                          self._parse_cmd('quit'))
        self.assertEqual(self.minibal.text, 'I quit!')

    def test_muc_empty_taunt(self):
        'Taunt someone from the MUC (empty tauntionary)'
        self.minibal.taunt(None, self._parse_cmd('taunt'))
        self.assertEqual(self.minibal.text, 'The tauntionary is empty')
        self.minibal.taunt(None, self._parse_cmd('taunt Hans'))
        self.assertEqual(self.minibal.text, 'The tauntionary is empty')

    def test_muc_taunt(self):
        'Taunt someone from the MUC (empty tauntionary)'
        self.minibal.tauntionary.add_taunt('blorgh!', 'Igor')

        self.minibal.taunt(None, self._parse_muc_cmd('taunt'))
        self.assertEqual(self.minibal.text, 'blorgh!')
        self.minibal.taunt(None, self._parse_muc_cmd('taunt Grichka'))
        self.assertEqual(self.minibal.text, 'Grichka: blorgh!')

    def test_add_invalid_taunt(self):
        'Add an invalid taunt'
        self.minibal.taunt(Message(),
                           self._parse_cmd('taunt -a blorgh!'))
        self.assertEqual(self.minibal.reply,
                         'error: Taunt: empty user nickname')

    def test_list_empty_taunt(self):
        'Ask for the (empty) list of taunts'
        self.minibal.taunt(Message(), self._parse_cmd('taunt -l'))
        self.assertEqual(self.minibal.reply, '\n')


if __name__ == '__main__':
    unittest.main()
