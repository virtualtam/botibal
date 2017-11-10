"""Botibal: a silly XMPP bot"""
import codecs
import decimal
import math
import re

from botibal.client.minibal import MiniBal


class BotiBal(MiniBal):
    """A silly XMPP bot"""

    # pylint: disable=too-many-public-methods

    def rot13(self, _, args):
        """Applies rot13 on the passed string"""
        self.say_group(codecs.encode(' '.join(args.text), 'rot_13'))

    def factorial(self, body):
        """Perpetuates the legacy of /u/ExpectedFactorialBot/. Well, kind of.

        Looks for chunks of text looking like factorial expressions, computes
        them and proudly tells the results to the world.

        Limitations/choices:
        - process 1- to 4-digit numbers only
        - big figures are displayed using the scientific notation
        """
        matches = re.findall(r'\d+\s?!', body, re.UNICODE)

        if matches == []:
            return False

        for match in matches:
            number = int(match[:-1].strip())
            if number > 9999:
                self.say_group("I like trains!")
                continue
            try:
                if number < 11:
                    self.say_group(
                        '{number}! = {factorial}'.format(
                            number=number,
                            factorial=math.factorial(number)
                        )
                    )
                    continue

                self.say_group(
                    '{number}! = {factorial:.2E}'.format(
                        number=number,
                        factorial=decimal.Decimal(math.factorial(number))
                    )
                )
            except ValueError:
                continue

        return True

    def add_common_commands(self, subparser):
        super(BotiBal, self).add_common_commands(subparser)

        p_rot13 = subparser.add_parser('rot13', help="returns a rot13'd string")
        p_rot13.add_argument('text', type=str, nargs='+')
        p_rot13.set_defaults(func=self.rot13)

    def muc_hook(self, msg):
        super(BotiBal, self).muc_hook(msg)

        if self.factorial(msg['body']):
            return True

        return False
