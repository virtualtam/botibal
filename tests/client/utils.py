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

    reply = ''
    text = ''

    def say_group(self, text):
        self.text = text

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
