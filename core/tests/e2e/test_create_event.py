from core.response_schemas import EventCreateResponse


EVENT_DATA_TEMPLATE = {
    "starts_at": "2022-06-01 20:00",
    "ends_at": "2022-06-01 21:00",
    "description": "Test meeting",
    "is_private": False,
    "is_recurrent": False
}


def test_create_event__with_correct_data_without__participants(
        client, main_user, main_user_credentials):
    # Создаем первого пользователя
    result = client.post("/signup/", json=main_user)
    your_id = result.json().get('id')

    # Логинимся за первого пользователя
    result = client.post(
        "/login/",
        data=main_user_credentials,
        headers={
            "Content-Type": "application/x-www-form-urlencoded"})

    token = result.json().get('access_token')
    authorization_headers = {"Authorization": f"Bearer {token}"}

    # Создаем встречу
    EVENT_DATA = dict(EVENT_DATA_TEMPLATE)
    EVENT_DATA['owner_id'] = your_id

    result = client.post(
        "/events/",
        json=EVENT_DATA,
        headers=authorization_headers)

    assert result.status_code == 201
    assert EventCreateResponse.validate(result.json())


def test_create_event__with_correct_data_with__participants(
        client, main_user, main_user_credentials, secondary_user):
    # Создаем первого пользователя
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
    EVENT_DATA = dict(EVENT_DATA_TEMPLATE)
    EVENT_DATA['owner_id'] = your_id
    EVENT_DATA['participants'] = [user_id]

    result = client.post(
        "/events/",
        json=EVENT_DATA,
        headers=authorization_headers)

    assert result.status_code == 201
    assert EventCreateResponse.validate(result.json())


def test_create_event__create_recurrent_yearly_event(
        client, main_user, main_user_credentials):
    # Создаем первого пользователя
    result = client.post("/signup/", json=main_user)
    your_id = result.json().get('id')

    # Логинимся за первого пользователя
    result = client.post(
        "/login/",
        data=main_user_credentials,
        headers={
            "Content-Type": "application/x-www-form-urlencoded"})

    token = result.json().get('access_token')
    authorization_headers = {"Authorization": f"Bearer {token}"}

    # Создаем встречу
    EVENT_DATA = dict(EVENT_DATA_TEMPLATE)
    EVENT_DATA['owner_id'] = your_id
    EVENT_DATA['recurrency_rule'] = 'yearly | True | interval | 1'

    result = client.post(
        "/events/",
        json=EVENT_DATA,
        headers=authorization_headers)

    assert result.status_code == 201
    assert EventCreateResponse.validate(result.json())


def test_create_event__create_recurrent_monthly_event(
        client, main_user, main_user_credentials):
    # Создаем первого пользователя
    result = client.post("/signup/", json=main_user)
    your_id = result.json().get('id')

    # Логинимся за первого пользователя
    result = client.post(
        "/login/",
        data=main_user_credentials,
        headers={
            "Content-Type": "application/x-www-form-urlencoded"})

    token = result.json().get('access_token')
    authorization_headers = {"Authorization": f"Bearer {token}"}

    # Создаем встречу
    EVENT_DATA = dict(EVENT_DATA_TEMPLATE)
    EVENT_DATA['owner_id'] = your_id
    EVENT_DATA['recurrency_rule'] = 'monthly | True | interval | 1'

    result = client.post(
        "/events/",
        json=EVENT_DATA,
        headers=authorization_headers)

    assert result.status_code == 201
    assert EventCreateResponse.validate(result.json())


def test_create_event__create_recurrent_daily_event(
        client, main_user, main_user_credentials):
    # Создаем первого пользователя
    result = client.post("/signup/", json=main_user)
    your_id = result.json().get('id')

    # Логинимся за первого пользователя
    result = client.post(
        "/login/",
        data=main_user_credentials,
        headers={
            "Content-Type": "application/x-www-form-urlencoded"})

    token = result.json().get('access_token')
    authorization_headers = {"Authorization": f"Bearer {token}"}

    # Создаем встречу
    EVENT_DATA = dict(EVENT_DATA_TEMPLATE)
    EVENT_DATA['owner_id'] = your_id
    EVENT_DATA['recurrency_rule'] = 'daily | True | interval | 1'

    result = client.post(
        "/events/",
        json=EVENT_DATA,
        headers=authorization_headers)

    assert result.status_code == 201
    assert EventCreateResponse.validate(result.json())


def test_create_event__create_recurrent_weekly_event(
        client, main_user, main_user_credentials):
    # Создаем первого пользователя
    result = client.post("/signup/", json=main_user)
    your_id = result.json().get('id')

    # Логинимся за первого пользователя
    result = client.post(
        "/login/",
        data=main_user_credentials,
        headers={
            "Content-Type": "application/x-www-form-urlencoded"})

    token = result.json().get('access_token')
    authorization_headers = {"Authorization": f"Bearer {token}"}

    # Создаем встречу
    EVENT_DATA = dict(EVENT_DATA_TEMPLATE)
    EVENT_DATA['owner_id'] = your_id
    EVENT_DATA['recurrency_rule'] = 'weekly | 0, 5, 6 | interval | 1'

    result = client.post(
        "/events/",
        json=EVENT_DATA,
        headers=authorization_headers)

    assert result.status_code == 201
    assert EventCreateResponse.validate(result.json())


def test_create_event__create_recurrent_event_with_wrong_rule(
        client, main_user, main_user_credentials):
    # Создаем первого пользователя
    result = client.post("/signup/", json=main_user)
    your_id = result.json().get('id')

    # Логинимся за первого пользователя
    result = client.post(
        "/login/",
        data=main_user_credentials,
        headers={
            "Content-Type": "application/x-www-form-urlencoded"})

    token = result.json().get('access_token')
    authorization_headers = {"Authorization": f"Bearer {token}"}

    # Создаем встречу
    EVENT_DATA = dict(EVENT_DATA_TEMPLATE)
    EVENT_DATA['owner_id'] = your_id
    EVENT_DATA['recurrency_rule'] = 'yearly: True, monthly: [1, 2, 3]'

    result = client.post(
        "/events/",
        json=EVENT_DATA,
        headers=authorization_headers)

    assert result.status_code == 400
