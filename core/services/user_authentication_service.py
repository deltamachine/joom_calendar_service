from typing import Union
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt

from core.services.user_service import UserService
from core.settings import settings
from core.utils import get_db
from core.models import User


oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"


class UserAuthenticationService:
    """
    Сервис для аутентификации пользователя.
    """

    def __init__(self, db):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.user_service = UserService(db)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Проверяет, что переданный пароль совпадает с хэшированным паролем в базе.
        """

        return self.pwd_context.verify(plain_password, hashed_password)

    def authenticate_user(self, username: str, password: str) -> Union[bool, User]:
        """
        Аутентифицирует пользователя.
        """

        try:
            user = self.user_service.get_user_by_email(username)
        except HTTPException:
            return False

        if not self.verify_password(password, user.hashed_password):
            return False

        return user

    def create_access_token(self, data: dict, expires_delta: Union[timedelta, None]) -> str:
        """
        Создает токен для пользователя.
        """

        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        return encoded_jwt

    @staticmethod
    def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)) -> User:
        """
        Проверяет, существует ли пользователь, передавший токен, в базе, и возвращает его.
        """

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("username")

            if username is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception

        user_service = UserService(db)
        user = user_service.get_user_by_email(username)

        if user is None:
            raise credentials_exception

        return user
