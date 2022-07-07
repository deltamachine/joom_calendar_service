EVENT_DATA = {
    "starts_at": "2022-06-01 20:00",
    "ends_at": "2022-06-01 21:00",
    "description": "Test meeting",
    "is_private": False,
    "is_recurrent": False
}


def test_accept_or_decline_invite__accept_my_invite(
        client,
        main_user,
        main_user_credentials,
        secondary_user,
        secondary_user_credentials):
    # Создаем пользователя 1, он же владелец встречи
    result = client.post("/signup/", json=main_user)
    your_id = result.json().get('id')

    # Создаем второго пользователя
    result = client.post("/signup/", json=secondary_user)
    user_id = result.json().get('id')

    # Логинимся за первого пользователя
    result = client.post(
        "/login/",
        data=main_user_credentials,
        headers={
            "Content-Type": "application/x-www-form-urlencoded"})

    token = result.json().get('access_token')
    authorization_headers = {"Authorization": f"Bearer {token}"}

    # Создаем встречу
    EVENT_DATA['owner_id'] = your_id
    EVENT_DATA['participants'] = [user_id]

    client.post("/events/", json=EVENT_DATA, headers=authorization_headers)

    # Логинимся за второго пользователя
    result = client.post(
        "/login/",
        data=secondary_user_credentials,
        headers={
            "Content-Type": "application/x-www-form-urlencoded"})

    token = result.json().get('access_token')
    authorization_headers = {"Authorization": f"Bearer {token}"}

    # Принимаем приглашение
    data = {
        "is_accepted": True
    }

    result = client.put("/invite/1/", json=data, headers=authorization_headers)

    assert result.status_code == 204


def test_accept_or_decline_invite__decline_my_invite(
        client,
        main_user,
        main_user_credentials,
        secondary_user,
        secondary_user_credentials):
    # Создаем первого пользователя, он же владелец встречи
    result = client.post("/signup/", json=main_user)
    your_id = result.json().get('id')

    # Создаем второго пользователя
    result = client.post("/signup/", json=secondary_user)
    user_id = result.json().get('id')

    # Логинимся за первого пользователя
    result = client.post(
        "/login/",
        data=main_user_credentials,
        headers={
            "Content-Type": "application/x-www-form-urlencoded"})

    token = result.json().get('access_token')
    authorization_headers = {"Authorization": f"Bearer {token}"}

    # Создаем встречу
    EVENT_DATA['owner_id'] = your_id
    EVENT_DATA['participants'] = [user_id]

    client.post("/events/", json=EVENT_DATA, headers=authorization_headers)

    # Логинимся за второго пользователя
    result = client.post(
        "/login/",
        data=secondary_user_credentials,
        headers={
            "Content-Type": "application/x-www-form-urlencoded"})

    token = result.json().get('access_token')
    authorization_headers = {"Authorization": f"Bearer {token}"}

    # Отклоняем приглашение
    data = {
        "is_accepted": False
    }

    result = client.put("/invite/1/", json=data, headers=authorization_headers)

    assert result.status_code == 204


def test_accept_or_decline_invite__decline_others_invite(
        client, main_user, main_user_credentials, secondary_user):
    # Создаем первого пользователя, он же владелец встречи
    result = client.post("/signup/", json=main_user)
    your_id = result.json().get('id')

    # Создаем второго пользователя
    result = client.post("/signup/", json=secondary_user)
    user_id = result.json().get('id')

    # Логинимся за первого пользователя
    result = client.post(
        "/login/",
        data=main_user_credentials,
        headers={
            "Content-Type": "application/x-www-form-urlencoded"})

    token = result.json().get('access_token')
    authorization_headers = {"Authorization": f"Bearer {token}"}

    # Создаем встречу
    EVENT_DATA['owner_id'] = your_id
    EVENT_DATA['participants'] = [user_id]

    client.post("/events/", json=EVENT_DATA, headers=authorization_headers)

    # Отклоняем чужое приглашение
    data = {
        "is_accepted": False
    }

    result = client.put("/invite/1/", json=data, headers=authorization_headers)

    assert result.status_code == 401
