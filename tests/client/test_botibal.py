# -*- coding: utf-8 -*-
'botibal.client.botibal unit tests'
# pylint: disable=too-many-public-methods
import unittest

from botibal.client.botibal_ import BotiBal

from tests.utils import DBTestCase


class TestBotiBal(DBTestCase):
    'Covers command parsing'
    def setUp(self):
        super(TestBotiBal, self).setUp()
        self.botibal = BotiBal('bot@server.org', 'p455w0rd', 'bot',
                               'room@server.org', 'admin@server.org',
                               self.test_db)

    def test_init(self):
        'Build-Bot :-)'
        BotiBal('bot@server.org', 'p455w0rd', 'bot',
                'room@server.org', 'admin@server.org', self.test_db)


if __name__ == '__main__':
    unittest.main()
