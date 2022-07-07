from fastapi import HTTPException

from core.models import Event, User
from core.services import UserService


class EventService:
    """
    Класс для работы с таблицей Event в базе данных
    """

    def __init__(self, db):
        self.db = db
        self.user_service = UserService(db)

    def create_event(self, data: dict) -> Event:
        """
        Создает пользователя в базе данных.
        """

        event = Event()

        event.starts_at = data.get('starts_at')
        event.ends_at = data.get('ends_at')
        event.description = data.get('description')
        event.is_private = data.get('is_private')
        event.is_recurrent = data.get('is_recurrent')
        event.owner_id = data.get('owner_id')
        event.recurrency_rule = data.get('recurrency_rule')

        participants = data.get('participants')

        if participants:
            for participant_id in participants:
                participant = self.db.query(User).get(participant_id)
                event.participants.append(participant)

        return event

    def insert_event(self, event: Event) -> Event:
        """
        Записывает пользователя в базу данных.
        """

        self.db.add(event)
        self.db.commit()

        self.db.refresh(event)

        return event

    def get_event(self, event_id: int) -> Event:
        """
        Возвращает событие по ID.
        """

        event = self.db.query(Event).get(event_id)

        if event:
            return event

        raise HTTPException(status_code=404,
                            detail='Событие с таким ID не найдено')
