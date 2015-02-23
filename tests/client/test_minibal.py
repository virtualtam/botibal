# -*- coding: utf-8 -*-
'botibal.client.minibal unit tests'
# pylint: disable=too-many-public-methods
import unittest

from botibal.client.minibal import MiniBal

from tests.utils import DBTestCase


class TestMiniBal(DBTestCase):
    'Covers command parsing'
    def setUp(self):
        super(TestMiniBal, self).setUp()
        self.minibal = MiniBal('bot@server.org', 'p455w0rd', 'bot',
                               'room@server.org', 'admin@server.org',
                               self.test_db)

    def test_init(self):
        'Build-Bot :-)'
        MiniBal('bot@server.org', 'p455w0rd', 'bot',
                'room@server.org', 'admin@server.org', self.test_db)


if __name__ == '__main__':
    unittest.main()
