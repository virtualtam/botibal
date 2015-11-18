# -*- coding: utf-8 -*-
"""
Bot entrypoint
"""
from __future__ import absolute_import, unicode_literals

import logging
import sys
from argparse import ArgumentParser

from . import BotiBal, MiniBal, QuizziBal

# pylint: disable=import-error
try:
    # Python 3
    from configparser import ConfigParser
except ImportError:
    # Python 2
    from ConfigParser import ConfigParser


def run():
    """
    Main Botibal entrypoint
    """
    parser = ArgumentParser()
    parser.add_argument(
        'config_file',
        help="configuration file"
    )
    parser.add_argument(
        'database_file',
        help="data storage file"
    )
    parser.add_argument(
        '-d', '--debug',
        help='set logging to DEBUG',
        action='store_const',
        dest='loglevel',
        const=logging.DEBUG,
        default=logging.INFO
    )
    kind = parser.add_mutually_exclusive_group(required=True)
    kind.add_argument(
        '-b', '--botibal',
        help="BotiBal, the Fukung-addict bot",
        action='store_true'
    )
    kind.add_argument(
        '-m', '--minibal',
        help="MiniBal, the minimalist bot",
        action='store_true'
    )
    kind.add_argument(
        '-q', '--quizzibal',
        help="QuizziBal, the quizzical bot",
        action='store_true'
    )

    args = parser.parse_args()

    config = ConfigParser()
    config.sections()
    config.read(args.config_file)

    if sys.version_info < (3, 0):
        # pylint: disable=import-error
        from sleekxmpp.util.misc_ops import setdefaultencoding
        setdefaultencoding('utf8')

    logging.basicConfig(
        level=args.loglevel,
        format='%(levelname)-8s %(message)s'
    )

    if args.botibal:
        bot = BotiBal(
            config['auth']['jid'],
            config['auth']['password'],
            config['nick']['botibal'],
            config['muc']['room'],
            config['muc']['admin_jid'],
            args.database_file
        )

    elif args.minibal:
        bot = MiniBal(
            config['auth']['jid'],
            config['auth']['password'],
            config['nick']['minibal'],
            config['muc']['room'],
            config['muc']['admin_jid'],
            args.database_file
        )

    elif args.quizzibal:
        bot = QuizziBal(
            config['auth']['jid'],
            config['auth']['password'],
            config['nick']['quizzibal'],
            config['muc']['room'],
            config['muc']['admin_jid'],
            args.database_file
        )

    if sys.version_info < (3, 0):
        # SleekXMPP
        if bot.connect(use_tls=config['sleekxmpp']['use_tls']):
            bot.process(block=True)
        else:
            logging.warning("Unable to connect")
    else:
        # SliXMPP
        bot.connect()
        bot.process(forever=True)
