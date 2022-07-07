from core.response_schemas import UserCreateResponse


BROKEN_USER_DATA = {
    "first_name": "Anya",
    "email": "test@gmail.com",
    "password": "12345",
}


def test_signup__with_correct_data(client, main_user):
    # Создаем пользователя с корректными данными
    response = client.post("/signup/", json=main_user)

    assert response.status_code == 201
    assert UserCreateResponse.validate(response.json())


def test_signup__with_broken_data(client):
    # Создаем пользователя с некорректными данными
    response = client.post("/signup/", json=BROKEN_USER_DATA)

    assert response.status_code == 422


def test_signup__with_already_existing_email(client, main_user):
    # Создаем пользователя с корректными данными
    response = client.post("/signup/", json=main_user)

    assert response.status_code == 201
    assert UserCreateResponse.validate(response.json())

    # Пытаемся создать его еще раз
    response = client.post("/signup/", json=main_user)

    assert response.status_code == 400
