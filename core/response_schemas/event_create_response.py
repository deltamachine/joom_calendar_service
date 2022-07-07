from pydantic import BaseModel

from core.models import Event


class EventCreateResponse(BaseModel):
    """
    Схема, описывающая ответ на вопрос о создании встречи.
    """

    id: int

    @staticmethod
    def make_serialized_item(event: Event) -> dict:
        result = {
            'id': event.id
        }

        return result

    @staticmethod
    def serializer(event: Event) -> dict:
        return EventCreateResponse.make_serialized_item(event)
