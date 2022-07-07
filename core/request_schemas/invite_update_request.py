from pydantic import BaseModel


class InviteUpdateRequest(BaseModel):
    """
    Схема, валидирующая запрос об отклике на приглашение.
    """

    is_accepted: bool
