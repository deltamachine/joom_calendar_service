from pydantic import BaseModel

from core.models import User


class UserResponse(BaseModel):
    """
    Схема, описывающая ответ на запрос о пользователе.
    """

    id: int
    first_name: str
    last_name: str
    email: str
    tz_offset: int

    @staticmethod
    def make_serialized_item(user: User) -> dict:
        result = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'tz_offset': user.tz_offset
        }

        return result

    @staticmethod
    def serializer(user: User) -> dict:
        return UserResponse.make_serialized_item(user)
