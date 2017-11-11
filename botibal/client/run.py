"""Bot entrypoint"""
import logging
from argparse import ArgumentParser
from configparser import ConfigParser

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from botibal import __title__, __version__
from botibal.models import Base

from . import BotiBal, MiniBal, QuizziBal


def run():
    """Main Botibal entrypoint"""
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
    parser.add_argument(
        '-v', '--version',
        help="display the program version",
        action='version',
        version='{} v{}'.format(__title__, __version__)
    )
    kind = parser.add_mutually_exclusive_group(required=True)
    kind.add_argument(
        '-b', '--botibal',
        help="BotiBal, the silly bot",
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
    config.read(args.config_file)

    logging.basicConfig(
        level=args.loglevel,
        format='%(levelname)-8s %(message)s'
    )

    engine = create_engine('sqlite:///%s' % args.database_file)
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()

    if args.botibal:
        bot = BotiBal(
            config['auth']['jid'],
            config['auth']['password'],
            config['nick']['botibal'],
            config['muc']['room'],
            config['muc']['admin_jid'],
            session
        )

    elif args.minibal:
        bot = MiniBal(
            config['auth']['jid'],
            config['auth']['password'],
            config['nick']['minibal'],
            config['muc']['room'],
            config['muc']['admin_jid'],
            session
        )

    elif args.quizzibal:
        bot = QuizziBal(
            config['auth']['jid'],
            config['auth']['password'],
            config['nick']['quizzibal'],
            config['muc']['room'],
            config['muc']['admin_jid'],
            session
        )

    bot.connect()
    bot.process(forever=True)
