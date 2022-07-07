from datetime import datetime
from typing import List, Union

from fastapi import Header, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from core.utils import get_db
from core.services import IntervalService, UserAuthenticationService
from core.response_schemas import EventResponse, InviteResponse
from core.models import User, Event, Invite
from .router import router


@router.get(
    '/events/',
    status_code=200,
    response_model=List[Union[EventResponse, InviteResponse]],
)
async def get_events_in_interval(user_id: int,
                                 from_time: str,
                                 to_time: str,
                                 db: Session = Depends(get_db),
                                 current_user: User = Depends(UserAuthenticationService.get_current_user)) -> JSONResponse:
    """
    Эндпойнт для получения всех встреч пользователя в заданный промежуток времени.
    """

    from_time = datetime.strptime(from_time, "%Y-%m-%d %H:%M")
    to_time = datetime.strptime(to_time, "%Y-%m-%d %H:%M")

    interval_service = IntervalService(db)
    events = interval_service.get_events_in_interval(user_id, from_time, to_time=to_time)

    result = []

    for item in events:
        if isinstance(item, Event):
            item = EventResponse.serializer(item, current_user)
        elif isinstance(item, Invite):
            item = InviteResponse.serializer(item, current_user)
        result.append(item)

    result = sorted(result, key=lambda x: x['starts_at'])

    return JSONResponse(result, status_code=200)
