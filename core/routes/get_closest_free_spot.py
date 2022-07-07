from typing import List, Union

from fastapi import Header, Depends, Request, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from core.utils import get_db
from core.services import FreeSpotService, UserAuthenticationService
from core.response_schemas import FreeSpotGetResponse
from core.models import User
from .router import router


@router.get(
    '/spots/',
    status_code=200,
    response_model=FreeSpotGetResponse,
)
async def get_closest_free_spot(meeting_length: int,
                                users: Union[List[int], None] = Query(default=None),
                                db: Session = Depends(get_db),
                                current_user: User = Depends(UserAuthenticationService.get_current_user)) -> JSONResponse:
    """
    Эндпойнт для получения ближайшего свободного интервала заданной длины в календарях пользователей.
    """

    spot_service = FreeSpotService(db)
    spot = spot_service.get_closest_free_spot(users, meeting_length)

    result = FreeSpotGetResponse.serializer(spot)

    return JSONResponse(result, status_code=200)
