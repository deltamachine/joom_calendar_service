from sqlalchemy import Column, Integer, String

from core.db import Base


class User(Base):
    """
    Модель для хранения информации о пользователе календаря.
    """

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(1000))
    last_name = Column(String(1000))
    email = Column(String(1000), unique=True, index=True)
    hashed_password = Column(String(1000))
    tz_offset = Column(Integer)

    def __str__(self):
        return f"User {self.id}: {self.first_name} {self.last_name}"
