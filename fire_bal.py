#!/usr/bin/env python2
"""
Start
"""
import config
import logging
import sys
from argparse import ArgumentParser

from botibal.client import BotiBal, MiniBal, QuizziBal

if __name__ == '__main__':
    PARSER = ArgumentParser()
    PARSER.add_argument('-d', '--debug', help='set logging to DEBUG',
                        action='store_const', dest='loglevel',
                        const=logging.DEBUG, default=logging.INFO)
    KIND = PARSER.add_mutually_exclusive_group(required=True)
    KIND.add_argument('-b', '--botibal',
                      help='BotiBal, the Fukung-addict bot',
                      action='store_true')
    KIND.add_argument('-m', '--minibal', help='MiniBal, the minimalist bot',
                      action='store_true')
    KIND.add_argument('-q', '--quizzibal', help='QuizziBal, the quizzical bot',
                      action='store_true')

    ARGS = PARSER.parse_args()

    if sys.version_info < (3, 0):
        from sleekxmpp.util.misc_ops import setdefaultencoding
        setdefaultencoding('utf8')

    logging.basicConfig(level=ARGS.loglevel,
                        format='%(levelname)-8s %(message)s')

    if ARGS.botibal:
        BOT = BotiBal(config.JID, config.PASSWORD, 'Botibal',
                      config.ROOM, config.ADMIN_JID)

    elif ARGS.minibal:
        BOT = MiniBal(config.JID, config.PASSWORD, 'Minibal',
                      config.ROOM, config.ADMIN_JID)

    elif ARGS.quizzibal:
        BOT = QuizziBal(config.JID, config.PASSWORD, 'Quizzibal',
                        config.ROOM, config.ADMIN_JID)

    if BOT.connect(use_tls=config.USE_TLS):
        BOT.process(block=True)
    else:
        print 'Unable to connect'
