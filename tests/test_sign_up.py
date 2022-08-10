from db import User, UserGroup
from fastapi.testclient import TestClient
from app import app, RequestBody
import pytest
from unittest.mock import patch


@pytest.fixture(scope='session')
def user_group(session):
    new = UserGroup(
        name='manager'
    )
    session.add(new)
    session.commit()
    return new


@pytest.fixture(scope='session')
def input_data(user_group):
    return RequestBody(
        first_name="Steven",
        last_name="Richardson",
        email="testrich@me.com",
        password="NotSoSimplePass",
        group_id=user_group.id
    )


# Тест успешно зарегистрированного пользователя
def test_signup_success(input_data, session):
    client = TestClient(app)
    with patch('db.session_factory') as patched:
        patched.return_value = session
        user = client.post('/signup', json=input_data.dict())

        assert user.status_code == 200

        db_user = session.query(User).filter_by(**user.json()).first()

        assert db_user, 'User has not registered'


# Тест на попытку регистрации по существующему в базе email'у
def test_signup_with_existing_email(input_data, session):

    client = TestClient(app)
    with patch('app.session_factory') as patched:
        patched.return_value = session
        user = client.post('/signup', json=input_data.dict())

    assert user.status_code == 409


# Тес на неправильный тип данных при попытке регистрации (email=5)
def test_validation_error():
    client = TestClient(app)
    user = client.post(
        '/signup',
        json={
            "first_name": "Steven",
            "last_name": "Richardson",
            "email": "testrich3@me.com",
            "password": "NotSoSimplePass",
            "group_id": 'manager'
        }
    )

    assert user.status_code == 422
