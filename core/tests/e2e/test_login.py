from core.response_schemas import TokenGetResponse


INCORRECT_CREDENTIALS = {'username': 'incorrect', 'password': 'incorrect'}


def test_login__with_correct_credentials(client, main_user, main_user_credentials):
    # Создаем пользователя
    client.post("/signup/", json=main_user)

    # Логинимся за пользователя
    response = client.post("/login/",
                           data=main_user_credentials,
                           headers={"Content-Type": "application/x-www-form-urlencoded"})

    assert response.status_code == 200
    assert TokenGetResponse.validate(response.json())


def test_login__with_incorrect_credentials(client):
    # Логинимся с неверными данными
    response = client.post("/login/",
                           data=INCORRECT_CREDENTIALS,
                           headers={"Content-Type": "application/x-www-form-urlencoded"})

    assert response.status_code == 401
