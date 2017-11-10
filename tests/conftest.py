"""Test fixtures"""
import sqlite3

import pytest


@pytest.fixture
def testdb():
    """Test database"""
    test_db = ':memory:'
    connection = sqlite3.connect(test_db)
    cursor = connection.cursor()

    yield test_db, connection, cursor

    connection.close()
