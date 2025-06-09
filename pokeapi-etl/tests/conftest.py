import pytest
import os
import sys
import logging
from unittest.mock import patch, MagicMock

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from data_models.models import Base
from utils.logging_config import setup_logging

TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="session")
def test_engine():
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture(scope="function")
def db_session():
    """Creates a new database session for a test.Rolls back everything after the test is done."""
    engine = create_engine(TEST_DATABASE_URL)
    Session = sessionmaker(bind=engine)

    Base.metadata.create_all(engine)

    session = Session()

    yield session

    session.close()
    Base.metadata.drop_all(engine)
