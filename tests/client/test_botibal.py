# -*- coding: utf-8 -*-
"""
botibal.client.botibal unit tests
"""
# pylint: disable=too-many-public-methods
import unittest

from botibal.client.botibal_ import BotiBal
from tests.client.utils import ClientTestCase, MockMiniBal

try:
    from sleekxmpp.stanza import Message
except ImportError:
    # pylint: disable=import-error
    from slixmpp.stanza import Message


class MockBotiBal(BotiBal, MockMiniBal):
    """
    Mock client for local testing
    """


class TestBotiBal(ClientTestCase):
    """
    Covers command parsing
    """

    def setUp(self):
        super(TestBotiBal, self).setUp()
        self.client = MockBotiBal('bot@server.org', 'p455w0rd', 'bot',
                                  'room@server.org', 'admin@server.org',
                                  self.test_db)

    def test_init(self):
        """
        Build-Bot :-)
        """
        BotiBal('bot@server.org', 'p455w0rd', 'bot',
                'room@server.org', 'admin@server.org', self.test_db)

    def test_rot13(self):
        """
        Grfgf Prfne'f pvcurevat
        """
        self.client.rot13(None,
                          self._parse_cmd("rot13 Grfgf Prfne'f pvcurevat"))
        self.assertEqual(self.client.text, "Tests Cesar's ciphering")

    def test_empty_fukung_list(self):
        """
        List fukung entries (empty list)
        """
        self.client.fukung_net(Message(), self._parse_cmd('fukung -l'))
        self.assertEqual(self.client.reply, '\n')

    def test_fukung_empty(self):
        """
        Display a link (empty list)
        """
        self.client.fukung_net(Message(), self._parse_cmd('fukung'))
        self.assertEqual(self.client.text,
                         'da fukung list iz empty! plz browse da intarnetz!')

    def test_fukung(self):
        """
        Display a link
        """
        self.client.fukung.add_link_id('1/test1.jpg')
        self.client.fukung_net(Message(), self._parse_muc_cmd('fukung'))
        self.assertEqual(self.client.text,
                         'http://www.fukung.net/v/1/test1.jpg')

    def test_fukung_add(self):
        """
        Add a link
        """
        link = 'http://www.fukung.net/v/3/test3.bmp'
        self.client.fukung_net(
            Message(),
            self._parse_cmd('fukung -a {}'.format(link)))
        self.assertEqual(str(self.client.fukung), '1 - {}'.format(link))

    def test_fukung_add_duplicate(self):
        """
        Add a link. Twice.
        """
        link = 'http://www.fukung.net/v/3/test3.bmp'
        self.client.fukung_net(
            Message(),
            self._parse_cmd('fukung -a {}'.format(link)))
        self.assertEqual(str(self.client.fukung), '1 - {}'.format(link))

        self.client.fukung_net(
            Message(),
            self._parse_cmd('fukung -a {}'.format(link)))
        self.assertEqual(self.client.reply, 'error: Duplicate Fukung link')


if __name__ == '__main__':
    unittest.main()
