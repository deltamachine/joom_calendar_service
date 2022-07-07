import pytest


@pytest.fixture
def secondary_user(secondary_user_credentials):
    secondary_user = {
        "first_name": "Vasya",
        "last_name": "Ivanov",
        "email": secondary_user_credentials.get("username"),
        "password": secondary_user_credentials.get("password"),
        "tz_offset": 0
    }

    return secondary_user
