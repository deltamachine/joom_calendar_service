from fastapi import Header, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from core.utils import get_db
from core.services import EventService, UserAuthenticationService
from core.response_schemas import EventResponse
from core.models import User
from .router import router


@router.get(
    '/events/{event_id}/',
    status_code=200,
    response_model=EventResponse,
)
async def get_event(event_id: int,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(UserAuthenticationService.get_current_user)) -> JSONResponse:
    """
    Эндпойнт для получения информации о событии по ID.
    """

    event_service = EventService(db)
    event = event_service.get_event(event_id)

    result = EventResponse.serializer(event, current_user)

    return JSONResponse(result, status_code=200)
