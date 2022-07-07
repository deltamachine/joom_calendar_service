from typing import List

from fastapi import HTTPException

from core.models import Invite
from core.services import UserService, EventService


class InviteService:
    """
    Класс для работы с таблицей Invite в базе данных
    """

    def __init__(self, db):
        self.db = db
        self.user_service = UserService(db)
        self.event_service = EventService(db)

    def create_invite(self, data: dict) -> Invite:
        """
        Создает приглашение.
        """

        invite = Invite()

        invite.invitee_id = data.get('invitee_id')
        invite.event_id = data.get('event_id')

        return invite

    def insert_invite(self, invite: Invite) -> dict:
        """
        Добавляет приглашение в базу данных.
        """

        self.db.add(invite)
        self.db.commit()

        self.db.refresh(invite)

        return invite

    def get_invite(self, invite_id: int) -> Invite:
        """
        Получает приглашение из базы данных по ID.
        """

        invite = self.db.query(Invite).get(invite_id)

        if invite:
            return invite

        raise HTTPException(status_code=404, detail='Событие с таким ID не найдено')

    def accept_or_decline_invite(self, invite_id: int, data: dict) -> None:
        """
        Записывает изменения о принятии или отклонении приглашения в базу данных.
        """

        invite = self.db.query(Invite).get(invite_id)

        try:
            invite.is_accepted = data.get('is_accepted')
            invite.is_viewed = True

            self.db.add(invite)
            self.db.commit()
        except AttributeError:
            raise HTTPException(status_code=404, detail='Событие с таким ID не найдено')


