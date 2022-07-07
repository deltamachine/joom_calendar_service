from fastapi import Depends, Response, HTTPException
from sqlalchemy.orm import Session

from core.services import InviteService, UserAuthenticationService
from core.request_schemas import InviteUpdateRequest
from core.utils import get_db
from core.models import User
from .router import router


@router.put("/invite/{invite_id}/", status_code=204)
async def accept_or_decline_invite(invite_id: int,
                                   data: InviteUpdateRequest,
                                   db: Session = Depends(get_db),
                                   current_user: User = Depends(UserAuthenticationService.get_current_user)) -> Response:
    """
    Эндпойнт для принятия или отклонения приглашения на встречу.
    """

    invite_service = InviteService(db)
    invite = invite_service.get_invite(invite_id)

    # Проверка прав
    if invite.invitee_id != current_user.id:
        raise HTTPException(
            status_code=401,
            detail="У вас нет прав на редактирование этого приглашения")

    # Изменение приглашения
    invite_service.accept_or_decline_invite(invite_id, data.dict())

    return Response(status_code=204)
