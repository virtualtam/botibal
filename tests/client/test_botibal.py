# -*- coding: utf-8 -*-
"""
botibal.client.botibal unit tests
"""
# pylint: disable=too-many-public-methods
import unittest

from slixmpp.stanza import Message

from botibal.client.botibal_ import BotiBal
from tests.client.utils import ClientTestCase, MockMiniBal


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

    def test_simple_factorial(self):
        """
        Simple string containing a little factorial to be computed
        """
        self.client.factorial("blah blah 6! and more blah")
        self.assertSayGroupEqual("6! = 720")

        self.client.factorial("10!")
        self.assertSayGroupEqual("10! = 3628800")

    def test_scientific_factorial(self):
        """
        Things are getting serious
        """
        self.client.factorial("OMG look at #11!")
        self.assertSayGroupEqual("11! = 3.99E+7")

        self.client.factorial("We're damn close to 9999!")
        self.assertSayGroupEqual("9999! = 2.85E+35655")

    def test_multiple_factorial(self):
        """
        Someone likes his sentences factorial-flavoured
        """
        self.client.factorial("blah blah 6! and more blah to 12! OK?")
        self.assertEqual(
            ["6! = 720", "12! = 4.79E+8"],
            self.client.muc_history[-2:]
        )

    def test_voulezvous_factorial(self):
        """
        Voulez-vous calculer avec moi ?
        """
        self.client.factorial("Plus que 2 !")
        self.assertSayGroupEqual("2! = 2")

    def test_donotwant_factorial(self):
        """
        Wow. So user input. Much do not want.
        """
        self.client.factorial("Do you believe it? He's getting 12345!")
        self.assertSayGroupEqual("I like trains!")

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
