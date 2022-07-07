from fastapi import Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from core.services import UserService
from core.request_schemas import UserCreateRequest
from core.response_schemas import UserCreateResponse
from core.utils import get_db
from .router import router


@router.post("/signup/", status_code=201, response_model=UserCreateResponse)
async def signup(data: UserCreateRequest,
                 db: Session = Depends(get_db)) -> JSONResponse:
    """
    Эндпойнт для создания нового пользователя.
    """

    user_service = UserService(db)
    user = user_service.create_user(data.dict())
    result = UserCreateResponse.serializer(user)

    return JSONResponse(result, status_code=201)
