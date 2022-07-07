from datetime import datetime, timedelta


MEETING_LENGTH = 60

EVENT_DATA_1 = {
    "starts_at": "2022-06-06 20:00",
    "ends_at": "2022-07-20 21:00",
    "description": "Test meeting",
    "is_private": False,
    "is_recurrent": False
}

EVENT_DATA_2 = {
    "starts_at": "2022-07-20 22:00",
    "ends_at": "2022-07-20 23:00",
    "description": "Test meeting",
    "is_private": False,
    "is_recurrent": False
}

EVENT_DATA_3 = {
    "starts_at": "2022-07-20 21:00",
    "ends_at": "2022-07-21 00:00",
    "description": "Test meeting",
    "is_private": False,
    "is_recurrent": False
}

NOW = datetime.now()
IN_HOUR = NOW + timedelta(minutes=MEETING_LENGTH)

EXPECTED_DATA_1 = {
    "starts_at": NOW.strftime("%Y-%m-%d %H:%M"),
    "ends_at": IN_HOUR.strftime("%Y-%m-%d %H:%M"),
}

EXPECTED_DATA_2 = {
    "starts_at": "2022-07-20 21:00",
    "ends_at": "2022-07-20 22:00"
}

EXPECTED_DATA_3 = {
    "starts_at": "2022-07-21 00:00",
    "ends_at": "2022-07-21 01:00"
}


def test_get_closest_free_spot__free_time_right_now(client, main_user, main_user_credentials,
                                                    secondary_user, secondary_user_credentials):
    """
    Потенциально flaky тест, зависит от текущего времени.
    """

    # Создаем первого пользователя
    result = client.post("/signup/", json=main_user)
    your_id = result.json().get('id')

    # Логинимся за первого пользователя
    result = client.post("/login/",
                         data=main_user_credentials,
                         headers={"Content-Type": "application/x-www-form-urlencoded"})

    token = result.json().get('access_token')
    authorization_headers = {"Authorization": f"Bearer {token}"}

    # Создаем встречу
    EVENT_1 = dict(EVENT_DATA_2)
    EVENT_1['owner_id'] = your_id

    client.post("/events/", json=EVENT_1, headers=authorization_headers)

    # Создаем второго пользователя
    result = client.post("/signup/", json=secondary_user)
    user_id = result.json().get('id')

    # Логинимся за второго пользователя
    result = client.post("/login/",
                         data=secondary_user_credentials,
                         headers={"Content-Type": "application/x-www-form-urlencoded"})

    token = result.json().get('access_token')
    authorization_headers = {"Authorization": f"Bearer {token}"}

    # Создаем встречу
    EVENT_2 = dict(EVENT_DATA_3)
    EVENT_2['owner_id'] = user_id

    client.post("/events/", json=EVENT_2, headers=authorization_headers)

    # Получаем ближайшее окно
    result = client.get(f"/spots/?users=1&users=2&meeting_length={MEETING_LENGTH}", headers=authorization_headers)

    assert result.json() == EXPECTED_DATA_1


def test_get_closest_free_spot__free_time_in_the_middle_of_meetings(client, main_user, main_user_credentials,
                                                                    secondary_user, secondary_user_credentials):
    # Создаем первого пользователя
    result = client.post("/signup/", json=main_user)
    your_id = result.json().get('id')

    # Логинимся за первого пользователя
    result = client.post("/login/",
                         data=main_user_credentials,
                         headers={"Content-Type": "application/x-www-form-urlencoded"})

    token = result.json().get('access_token')
    authorization_headers = {"Authorization": f"Bearer {token}"}

    # Создаем встречу
    EVENT_1 = dict(EVENT_DATA_1)
    EVENT_1['owner_id'] = your_id

    client.post("/events/", json=EVENT_1, headers=authorization_headers)

    # Создаем второго пользователя
    result = client.post("/signup/", json=secondary_user)
    user_id = result.json().get('id')

    # Логинимся за второго пользователя
    result = client.post("/login/",
                         data=secondary_user_credentials,
                         headers={"Content-Type": "application/x-www-form-urlencoded"})

    token = result.json().get('access_token')
    authorization_headers = {"Authorization": f"Bearer {token}"}

    # Создаем встречу
    EVENT_2 = dict(EVENT_DATA_2)
    EVENT_2['owner_id'] = user_id

    client.post("/events/", json=EVENT_2, headers=authorization_headers)

    # Получаем ближайшее окно
    result = client.get(f"/spots/?users=1&users=2&meeting_length={MEETING_LENGTH}", headers=authorization_headers)

    assert result.json() == EXPECTED_DATA_2


def test_get_closest_free_spot__free_time_after_all_events(client, main_user, main_user_credentials,
                                                           secondary_user, secondary_user_credentials):
    # Создаем первого пользователя
    result = client.post("/signup/", json=main_user)
    your_id = result.json().get('id')

    # Логинимся за первого пользователя
    result = client.post("/login/",
                         data=main_user_credentials,
                         headers={"Content-Type": "application/x-www-form-urlencoded"})

    token = result.json().get('access_token')
    authorization_headers = {"Authorization": f"Bearer {token}"}

    # Создаем встречу
    EVENT_1 = dict(EVENT_DATA_1)
    EVENT_1['owner_id'] = your_id

    EVENT_2 = dict(EVENT_DATA_2)
    EVENT_2['owner_id'] = your_id

    client.post("/events/", json=EVENT_1, headers=authorization_headers)
    client.post("/events/", json=EVENT_1, headers=authorization_headers)

    # Создаем второго пользователя
    result = client.post("/signup/", json=secondary_user)
    user_id = result.json().get('id')

    # Логинимся за второго пользователя
    result = client.post("/login/",
                         data=secondary_user_credentials,
                         headers={"Content-Type": "application/x-www-form-urlencoded"})

    token = result.json().get('access_token')
    authorization_headers = {"Authorization": f"Bearer {token}"}

    # Создаем встречу
    EVENT_3 = dict(EVENT_DATA_3)
    EVENT_3['owner_id'] = user_id

    client.post("/events/", json=EVENT_3, headers=authorization_headers)

    # Получаем ближайшее окно
    result = client.get(f"/spots/?users=1&users=2&meeting_length={MEETING_LENGTH}", headers=authorization_headers)

    assert result.json() == EXPECTED_DATA_3
