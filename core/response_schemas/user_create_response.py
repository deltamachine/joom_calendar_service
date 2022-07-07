from pydantic import BaseModel

from core.models import User


class UserCreateResponse(BaseModel):
    """
    Схема, описывающая ответ на запрос о создании пользователя.
    """

    id: int

    @staticmethod
    def make_serialized_item(user: User) -> dict:
        result = {
            'id': user.id
        }

        return result

    @staticmethod
    def serializer(user: User) -> dict:
        return UserCreateResponse.make_serialized_item(user)
