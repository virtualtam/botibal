# -*- coding: utf-8 -*-
"""
botibal.client test utilities
"""
# pylint: disable=too-many-public-methods
from botibal.client.minibal import MiniBal
from tests.utils import DBTestCase


class MockMiniBal(MiniBal):
    """
    Mock client for local testing
    """

    def __init__(self, jid, password, nick, room, admin_jid, database):
        # pylint: disable=too-many-arguments
        super(MockMiniBal, self).__init__(
            jid, password, nick, room, admin_jid, database
        )
        self.reply = ''
        self.muc_history = []

    @property
    def text(self):
        """
        Last message sent to the MUC
        """
        try:
            return self.muc_history[-1]
        except IndexError:
            return ''

    def say_group(self, text):
        self.muc_history.append(text)

    def send_reply(self, msg, text):
        self.reply = text

    def disconnect(self, wait=None):
        # pylint: disable=arguments-differ
        pass


class ClientTestCase(DBTestCase):
    """
    Client testing utilities
    """

    # pylint: disable=invalid-name

    client = None

    def _parse_cmd(self, cmd):
        """
        Parses a PM command
        """
        return self.client.cmd_parser.parse_args(cmd.split(' '))

    def _parse_muc_cmd(self, cmd):
        """
        Parses a MUC command
        """
        return self.client.muc_cmd_parser.parse_args(cmd.split(' '))

    def assertReplyEqual(self, text):
        """
        Asserts client.send_reply() has been called
        """
        self.assertEqual(self.client.reply, text)

    def assertSayGroupEqual(self, text):
        """
        Asserts client.say_group() has been called
        """
        self.assertEqual(self.client.text, text)
