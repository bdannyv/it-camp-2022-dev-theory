import pytest
from db import session_factory, User, UserGroup
from unittest.mock import patch


@pytest.fixture(scope='session')
def session():
    with session_factory() as sa_session:
        yield sa_session

        sa_session.rollback()
        sa_session.query(User).delete()
        sa_session.query(UserGroup).delete()
        sa_session.commit()
        sa_session.close()
