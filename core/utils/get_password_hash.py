from passlib.context import CryptContext


def get_password_hash(password: str) -> str:
    """
    Хэширует пароль пользователя.
    """

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    return pwd_context.hash(password)
