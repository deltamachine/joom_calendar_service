from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from core.services import EventService, InviteService, UserAuthenticationService, RecurrencyMetaService
from core.request_schemas import EventCreateRequest
from core.response_schemas import EventCreateResponse
from core.utils import get_db
from core.models import User
from .router import router


@router.post("/events/", status_code=201, response_model=EventCreateResponse)
async def create_event(data: EventCreateRequest,
                       db: Session = Depends(get_db),
                       current_user: User = Depends(UserAuthenticationService.get_current_user)) -> JSONResponse:
    """
    Эндпойнт для создания события в календаре.
    """

    # Проверка прав
    if current_user.id != data.owner_id:
        raise HTTPException(
            status_code=401,
            detail="Вы не можете создавать встречи от лица другого пользователя")

    # Создание встречи
    event_service = EventService(db)
    event = event_service.create_event(data.dict())
    event = event_service.insert_event(event)

    # Создание приглашений
    invite_service = InviteService(db)
    participants = data.participants

    if participants:
        for participant_id in participants:
            data = {
                "event_id": event.id,
                "invitee_id": participant_id
            }

            invite = invite_service.create_invite(data)
            invite_service.insert_invite(invite)

    # Создаем правила повторения
    if event.is_recurrent:
        meta_service = RecurrencyMetaService(db)
        metas = meta_service.create_recurrency_meta(event)
        meta_service.insert_many_recurrency_meta(metas)

    result = EventCreateResponse.serializer(event)

    return JSONResponse(result, status_code=201)
