# -*- coding: utf-8 -*-
'botibal.client.quizzibal unit tests'
# pylint: disable=too-many-public-methods
import unittest

from botibal.client.quizzibal import QuizziBal

from tests.utils import DBTestCase


class TestQuizziBal(DBTestCase):
    'Covers command parsing'
    def setUp(self):
        super(TestQuizziBal, self).setUp()
        self.quizzibal = QuizziBal('bot@server.org', 'p455w0rd', 'bot',
                                   'room@server.org', 'admin@server.org',
                                   self.test_db)

    def test_init(self):
        'Build-Bot :-)'
        QuizziBal('bot@server.org', 'p455w0rd', 'bot',
                  'room@server.org', 'admin@server.org', self.test_db)


if __name__ == '__main__':
    unittest.main()
