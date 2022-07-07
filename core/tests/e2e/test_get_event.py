EVENT_DATA = {
    "starts_at": "2022-06-01 20:00",
    "ends_at": "2022-06-01 21:00",
    "description": "Test meeting",
    "is_private": False,
    "is_recurrent": False
}

EXPECTED_DATA = {
    "id": 1,
    "starts_at": "2022-06-01 20:00",
    "ends_at": "2022-06-01 21:00",
    "description": "Test meeting",
    "is_private": False,
    "is_recurrent": False,
    "owner": {
        "id": 1,
        "first_name": "Anya",
        "last_name": "Kondrateva",
        "email": "anya@gmail.com",
        "tz_offset": 10800
    },
    "participants": [
        {
            "id": 2,
            "first_name": "Vasya",
            "last_name": "Ivanov",
            "email": "vasya@gmail.com",
            "tz_offset": 10800
        }
    ]
}

FAKE_ID = 2


def test_get_event__existing(client, main_user, main_user_credentials, secondary_user):
    # Создаем первого пользователя
    result = client.post("/signup/", json=main_user)
    your_id = result.json().get('id')

    # Создаем второго пользователя
    result = client.post("/signup/", json=secondary_user)
    user_id = result.json().get('id')

    # Логинимся за первого пользователя
    result = client.post("/login/",
                         data=main_user_credentials,
                         headers={"Content-Type": "application/x-www-form-urlencoded"})

    token = result.json().get('access_token')
    authorization_headers = {"Authorization": f"Bearer {token}"}

    # Создаем встречу
    EVENT_DATA['owner_id'] = your_id
    EVENT_DATA['participants'] = [user_id]

    result = client.post("/events/", headers=authorization_headers, json=EVENT_DATA)

    event_id = result.json().get('id')

    # Достаем встречу
    result = client.get(f"/events/{event_id}/", headers=authorization_headers)
    result = result.json()

    assert result == EXPECTED_DATA


def test_get_event__non_existing__with_token(client, main_user, main_user_credentials):
    # Создаем пользователя
    client.post("/signup/", json=main_user)

    # Логинимся за пользователя
    result = client.post("/login/",
                         data=main_user_credentials,
                         headers={"Content-Type": "application/x-www-form-urlencoded"})

    token = result.json().get('access_token')
    authorization_headers = {"Authorization": f"Bearer {token}"}

    # Пытаемся получить несуществующую встречу
    result = client.get(f"/events/{FAKE_ID}/", headers=authorization_headers)

    assert result.status_code == 404


def test_get_event__non_existing__without_token(client):
    # Пытаемся получить несуществующую встречу, не залогинившись
    result = client.get(f"/events/{FAKE_ID}/")

    assert result.status_code == 401
