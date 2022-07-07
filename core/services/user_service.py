from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from core.models import User
from core.utils import get_password_hash


class UserService:
    """
    Класс для работы с таблицей User в базе данных
    """

    def __init__(self, db):
        self.db = db

    def create_user(self, data: dict) -> User:
        """
        Функция, создающая пользователя в базе данных.
        """

        user = User()
        user.first_name = data.get("first_name")
        user.last_name = data.get("last_name")
        user.tz_offset = data.get("tz_offset")
        user.email = data.get("email")
        user.hashed_password = get_password_hash(data.get("password"))

        try:
            self.db.add(user)
            self.db.commit()

            self.db.refresh(user)

            return user
        except IntegrityError:
            raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует")

    def get_user_by_email(self, email: str) -> User:
        """
        Функция, ищущая и возвращающая пользователя с заданным емэйлом.
        """

        user = self.db.query(User).filter_by(email=email).first()

        if user:
            return user

        raise HTTPException(status_code=404, detail='Пользователь с таким email не найден')

    def get_user(self, user_id: int) -> User:
        """
        Функция, ищущая и возвращающая пользователя с заданным ID.
        """

        user = self.db.query(User).get(user_id)

        if user:
            return user

        raise HTTPException(status_code=404, detail='Пользователь с таким ID не найден')