from typing import List, Optional

from pydantic import BaseModel

from core.models import Event, User
from core.response_schemas.user_response import UserResponse


class EventResponse(BaseModel):
    """
    Схема, описывающая ответ на запрос о получении встречи.
    """

    id: int
    starts_at: str
    ends_at: str
    owner_id: dict
    participants: Optional[List[dict]]
    description: Optional[str]
    is_private: bool
    is_recurrent: bool

    @staticmethod
    def make_serialized_item(event: Event, hide_private=False) -> dict:
        result = {
            "id": event.id,
            'starts_at': event.starts_at.strftime("%Y-%m-%d %H:%M"),
            'ends_at': event.ends_at.strftime("%Y-%m-%d %H:%M"),
            'description': "busy" if hide_private else event.description,
            'owner': UserResponse.serializer(
                event.owner),
            'participants': [] if hide_private or not event.participants else [
                UserResponse.serializer(participant) for participant in event.participants],
            'is_private': event.is_private,
            'is_recurrent': event.is_recurrent}

        return result

    @staticmethod
    def serializer(event: Event, current_user: User) -> dict:
        if current_user.id != event.owner_id and event.is_private:
            return EventResponse.make_serialized_item(event, hide_private=True)
        else:
            return EventResponse.make_serialized_item(event)
