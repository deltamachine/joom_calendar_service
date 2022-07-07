from typing import List, Optional

from pydantic import BaseModel

from core.models import Invite, User
from core.response_schemas import EventResponse


class InviteResponse(BaseModel):
    """
    Схема, описывающая ответ на запрос о получении встречи, на которую пользователь был приглашен.
    """

    id: int
    starts_at: str
    ends_at: str
    owner_id: dict
    participants: Optional[List[dict]]
    description: Optional[str]
    is_private: bool
    is_recurrent: bool
    invite_id: int
    is_viewed: bool
    is_accepted: bool

    @staticmethod
    def make_serialized_item(invite: Invite, current_user: User) -> dict:
        event = invite.event
        result = EventResponse.serializer(event, current_user)

        result['invite_id'] = invite.id
        result['is_accepted'] = invite.is_accepted
        result['is_viewed'] = invite.is_viewed

        return result

    @staticmethod
    def serializer(invite: Invite, current_user: User) -> dict:
        return InviteResponse.make_serialized_item(invite, current_user)
