
EVENT_1_DATA = {
    "starts_at": "2022-06-01 20:00",
    "ends_at": "2022-06-01 21:00",
    "description": "Test meeting",
    "is_private": False,
    "is_recurrent": False,
}

EVENT_2_DATA = {
    "starts_at": "2022-06-01 22:00",
    "ends_at": "2022-06-01 23:00",
    "description": "Test meeting 2",
    "is_private": False,
    "is_recurrent": False,
}

EVENT_3_DATA = {
    "starts_at": "2022-05-25 21:00",
    "ends_at": "2022-05-25 22:00",
    "description": "Recurrent meeting",
    "is_private": False,
    "is_recurrent": True,
    "recurrency_rule": "weekly | 2, 3 | interval | 1"
}

INTERVAL_START = "2022-06-01 19:00"
INTERVAL_END = "2022-06-07 00:00"

EXPECTED_DATA_1 = [
    {
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
                "tz_offset": 0
            }
        ]
    },
    {
        "id": 2,
        "starts_at": "2022-06-01 22:00",
        "ends_at": "2022-06-01 23:00",
        "description": "Test meeting 2",
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
                "tz_offset": 0
            }
        ]
    }
]

EXPECTED_DATA_2 = [
    {
        "id": 1,
        "starts_at": "2022-06-01 20:00",
        "ends_at": "2022-06-01 21:00",
        "description": "Test meeting",
        "is_private": False,
        "is_recurrent": False,
        "owner": {
            "id": 2,
            "first_name": "Vasya",
            "last_name": "Ivanov",
            "email": "vasya@gmail.com",
            "tz_offset": 0
        },
        "participants": [
            {
                "id": 1,
                "first_name": "Anya",
                "last_name": "Kondrateva",
                "email": "anya@gmail.com",
                "tz_offset": 10800
            }
        ]
    },
    {
        "id": 2,
        "starts_at": "2022-06-01 22:00",
        "ends_at": "2022-06-01 23:00",
        "description": "busy",
        "is_private": True,
        "is_recurrent": False,
        "owner": {
            "id": 2,
            "first_name": "Vasya",
            "last_name": "Ivanov",
            "email": "vasya@gmail.com",
            "tz_offset": 0
        },
        "participants": []
    }
]

EXPECTED_DATA_3 = [
    {
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
        "participants": []
    },
    {
        "id": 2,
        "invite_id": 1,
        "starts_at": "2022-06-01 22:00",
        "ends_at": "2022-06-01 23:00",
        "description": "Test meeting 2",
        "is_private": False,
        "is_recurrent": False,
        "owner": {
            "id": 2,
            "first_name": "Vasya",
            "last_name": "Ivanov",
            "email": "vasya@gmail.com",
            "tz_offset": 0
        },
        "participants": [
            {
                "id": 1,
                "first_name": "Anya",
                "last_name": "Kondrateva",
                "email": "anya@gmail.com",
                "tz_offset": 10800
            }
        ],
        "is_accepted": False,
        "is_viewed": False,
    }
]

EXPECTED_DATA_4 = [
    {
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
        "participants": []
    },
    {
        "id": 2,
        "starts_at": "2022-06-01 21:00",
        "ends_at": "2022-06-01 22:00",
        "description": "Recurrent meeting",
        "is_private": False,
        "is_recurrent": True,
        "owner": {
            "id": 1,
            "first_name": "Anya",
            "last_name": "Kondrateva",
            "email": "anya@gmail.com",
            "tz_offset": 10800
        },
        "participants": []
    },
    {
        "id": 2,
        "starts_at": "2022-06-02 21:00",
        "ends_at": "2022-06-02 22:00",
        "description": "Recurrent meeting",
        "is_private": False,
        "is_recurrent": True,
        "owner": {
            "id": 1,
            "first_name": "Anya",
            "last_name": "Kondrateva",
            "email": "anya@gmail.com",
            "tz_offset": 10800
        },
        "participants": []
    },
]


def test_get_events_in_interval__get_current_user_events(client, main_user, main_user_credentials,
                                                         secondary_user):
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

    # Создаем встречи
    EVENT_1 = dict(EVENT_1_DATA)
    EVENT_2 = dict(EVENT_2_DATA)

    EVENT_1['owner_id'] = your_id
    EVENT_2['owner_id'] = your_id
    EVENT_1['participants'] = [user_id]
    EVENT_2['participants'] = [user_id]

    client.post("/events/", headers=authorization_headers, json=EVENT_1)
    client.post("/events/", headers=authorization_headers, json=EVENT_2)

    # Получаем свои встречи
    result = client.get(f"/events/?user_id={your_id}&from_time={INTERVAL_START}&to_time={INTERVAL_END}",
                        headers=authorization_headers)
    result = result.json()

    assert result == EXPECTED_DATA_1


def test_get_events_in_interval__get_other_user_events(client, main_user, main_user_credentials,
                                                       secondary_user, secondary_user_credentials):
    # Создаем первого пользователя
    result = client.post("/signup/", json=main_user)
    your_id = result.json().get('id')

    EVENT_1 = dict(EVENT_1_DATA)
    EVENT_2 = dict(EVENT_2_DATA)
    EVENT_1['participants'] = [your_id]
    EVENT_2['participants'] = [your_id]

    # Создаем второго пользователя
    result = client.post("/signup/", json=secondary_user)
    user_id = result.json().get('id')

    EVENT_1['owner_id'] = user_id
    EVENT_2['owner_id'] = user_id
    EVENT_2['is_private'] = True

    # Логинимся за второго пользователя
    result = client.post("/login/",
                         data=secondary_user_credentials,
                         headers={"Content-Type": "application/x-www-form-urlencoded"})

    token = result.json().get('access_token')
    authorization_headers = {"Authorization": f"Bearer {token}"}

    # Создаем встречи
    client.post("/events/", headers=authorization_headers, json=EVENT_1)
    client.post("/events/", headers=authorization_headers, json=EVENT_2)

    # Логинимся за первого пользователя
    result = client.post("/login/",
                         data=main_user_credentials,
                         headers={"Content-Type": "application/x-www-form-urlencoded"})

    token = result.json().get('access_token')
    authorization_headers = {"Authorization": f"Bearer {token}"}

    # Смотрим встречи второго пользователя
    result = client.get(f"/events/?user_id={user_id}&from_time={INTERVAL_START}&to_time={INTERVAL_END}",
                        headers=authorization_headers)
    result = result.json()

    assert result == EXPECTED_DATA_2


def test_get_events_in_interval__get_events_with_invites(client, main_user, main_user_credentials,
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

    # Создаем первую встречу
    EVENT_1 = dict(EVENT_1_DATA)
    EVENT_1['owner_id'] = your_id

    client.post("/events/", headers=authorization_headers, json=EVENT_1)

    # Создаем второго пользователя
    result = client.post("/signup/", json=secondary_user)
    user_id = result.json().get('id')

    # Логинимся за второго пользователя
    result = client.post("/login/",
                         data=secondary_user_credentials,
                         headers={"Content-Type": "application/x-www-form-urlencoded"})

    token = result.json().get('access_token')
    authorization_headers = {"Authorization": f"Bearer {token}"}

    # Создаем вторую встречу
    EVENT_2 = dict(EVENT_2_DATA)
    EVENT_2['owner_id'] = user_id
    EVENT_2['participants'] = [your_id]

    client.post("/events/", headers=authorization_headers, json=EVENT_2)

    # Логинимся за первого пользователя
    result = client.post("/login/",
                         data=main_user_credentials,
                         headers={"Content-Type": "application/x-www-form-urlencoded"})

    token = result.json().get('access_token')
    authorization_headers = {"Authorization": f"Bearer {token}"}

    # Просматриваем встречи
    result = client.get(f"/events/?user_id={your_id}&from_time={INTERVAL_START}&to_time={INTERVAL_END}",
                        headers=authorization_headers)
    result = result.json()

    assert result == EXPECTED_DATA_3


def test_get_events_in_interval__get_current_user_events_with_recurrent(client, main_user, main_user_credentials):
    # Создаем первого пользователя
    result = client.post("/signup/", json=main_user)
    your_id = result.json().get('id')

    # Логинимся за первого пользователя
    result = client.post("/login/",
                         data=main_user_credentials,
                         headers={"Content-Type": "application/x-www-form-urlencoded"})

    token = result.json().get('access_token')
    authorization_headers = {"Authorization": f"Bearer {token}"}

    # Создаем встречи
    EVENT_1 = dict(EVENT_1_DATA)
    EVENT_3 = dict(EVENT_3_DATA)

    EVENT_1['owner_id'] = your_id
    EVENT_3['owner_id'] = your_id

    client.post("/events/", headers=authorization_headers, json=EVENT_1)
    client.post("/events/", headers=authorization_headers, json=EVENT_3)

    # Получаем свои встречи
    result = client.get(f"/events/?user_id={your_id}&from_time={INTERVAL_START}&to_time={INTERVAL_END}",
                        headers=authorization_headers)
    result = result.json()

    assert result == EXPECTED_DATA_4
