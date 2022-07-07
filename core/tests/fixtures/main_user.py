import pytest


@pytest.fixture
def main_user(main_user_credentials):
    main_user = {
        "first_name": "Anya",
        "last_name": "Kondrateva",
        "email": main_user_credentials.get("username"),
        "password": main_user_credentials.get("password"),
        "tz_offset": 10800
    }

    return main_user
