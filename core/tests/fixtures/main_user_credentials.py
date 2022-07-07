import pytest


@pytest.fixture
def main_user_credentials():
    main_user_credentials = {
        "username": "anya@gmail.com",
        "password": "12345"
    }

    return main_user_credentials
