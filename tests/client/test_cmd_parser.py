# -*- coding: utf-8 -*-
"""
botibal.client.cmd_parser unit tests
"""
# pylint: disable=too-many-public-methods
import unittest

from botibal.client.cmd_parser import BotCmdError, BotCmdParser, BotHelp


class TestBotCmdParser(unittest.TestCase):
    """
    Test PM/MUC command parsing
    """

    def setUp(self):
        self.parser = BotCmdParser('test')

    def test_bot_help(self):
        """
        Ensure an exception is raised when the user asks for help
        """
        with self.assertRaises(BotHelp):
            self.parser.parse_args(['-h'])
        with self.assertRaises(BotHelp):
            self.parser.parse_args(['--help'])

    def test_invalid_option(self):
        """
        Ensure an exception is raised when an invalid option is passed
        """
        with self.assertRaises(BotCmdError):
            self.parser.parse_args(['--test'])


if __name__ == '__main__':
    unittest.main()
