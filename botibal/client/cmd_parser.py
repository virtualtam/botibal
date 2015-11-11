# -*- coding: utf-8 -*-
"""
Bot command parsing utilities
"""
from argparse import ArgumentParser


class BotCmdError(Exception):
    """
    Raised when invalid commands are passed

    The bot should catch this exception and reply to the user who emitted
    an invalid command.
    """


class BotHelp(BotCmdError):
    """
    Raised when the user asks for help
    """


class PrivilegeError(Exception):
    """
    Raised when a mere user attempts to run admin commands
    """


class BotCmdParser(ArgumentParser):
    """
    Parser for bot commands
    """

    def __init__(self, prog):
        super(BotCmdParser, self).__init__(prog=prog,
                                           add_help=False)
        self.add_argument('-h', '--help', action='help',
                          help='display bot command help')

    def error(self, message):
        raise BotCmdError(message)

    def print_help(self, *args):
        raise BotHelp(self.format_help(*args))
