import pytest


@pytest.fixture
def secondary_user_credentials():
    secondary_user_credentials = {
        "username": "vasya@gmail.com",
        "password": "54321"
    }

    return secondary_user_credentials
