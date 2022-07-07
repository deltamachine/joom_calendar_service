from pydantic import BaseModel


class UserCreateRequest(BaseModel):
    """
    Схема, валидирующая запрос на создание пользователя.
    """

    first_name: str
    last_name: str
    email: str
    password: str
    tz_offset: int
