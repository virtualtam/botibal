"""Test fixtures"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from botibal.models import Base


@pytest.fixture
def testdb():
    """Test database"""
    test_db = ':memory:'
    engine = create_engine('sqlite:///%s' % test_db)
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()

    yield test_db, session

    session.close()
