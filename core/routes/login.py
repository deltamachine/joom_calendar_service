from datetime import timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from core.services import UserAuthenticationService
from core.settings import settings
from core.response_schemas import TokenGetResponse
from core.utils import get_db
from .router import router


@router.post("/login/", response_model=TokenGetResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                db: Session = Depends(get_db)) -> JSONResponse:
    """
    Эндпойнт для аутентификации пользователя.
    """

    auth_service = UserAuthenticationService(db)
    user = auth_service.authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.access_token_expires_in_minutes)
    access_token = auth_service.create_access_token(
        data={"username": user.email}, expires_delta=access_token_expires
    )

    result = {"access_token": access_token, "token_type": "bearer"}

    return JSONResponse(result, status_code=200)
