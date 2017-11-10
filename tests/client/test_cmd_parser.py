"""botibal.client.cmd_parser unit tests"""
import pytest

from botibal.client.cmd_parser import BotCmdError, BotCmdParser, BotHelp


def test_bot_help():
    """Ensure an exception is raised when the user asks for help"""
    with pytest.raises(BotHelp):
        BotCmdParser('test').parse_args(['-h'])
    with pytest.raises(BotHelp):
        BotCmdParser('test').parse_args(['--help'])


def test_invalid_option():
    """Ensure an exception is raised when an invalid option is passed"""
    with pytest.raises(BotCmdError):
        BotCmdParser('test').parse_args(['--test'])
