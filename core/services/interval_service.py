from typing import List, Union
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from core.models import Event, Invite, RecurrencyMeta


class IntervalService:
    """
    Класс для работы с таблицей Event в базе данных
    """

    def __init__(self, db):
        self.db = db
        self.result = []

    def add_to_result(self, user_id: int, event: Event, invite: Invite):
        """
        Добавляет встречу / инвайт к текущему результату
        """

        if event and event.owner_id == user_id:
            self.result.append(event)
        elif invite and invite.invitee_id == user_id:
            self.result.append(invite)

    def filter_events(self, user_id: int, to_time: datetime = None) -> List[Event]:
        """
        Фильтрует события в календаре.
        """

        events = self.db.query(Event, RecurrencyMeta, Invite) \
            .join(RecurrencyMeta, isouter=True) \
            .join(Invite, isouter=True) \
            .filter((Event.owner_id == user_id) | (
                (Invite.invitee_id == user_id) & (Invite.is_viewed.is_(False) | (Invite.is_accepted.is_(True)))))\

        if to_time:
            events = events.filter(Event.starts_at < to_time)

        events = events.order_by(Event.starts_at).all()

        return events

    def copy_event(self, event: Event):
        """
        Копирует событие в новый объект класса Event.
        """

        rec_event = Event()
        rec_event.id = event.id
        rec_event.description = event.description
        rec_event.is_private = event.is_private
        rec_event.is_recurrent = event.is_recurrent
        rec_event.owner = event.owner
        rec_event.owner_id = event.owner_id
        rec_event.participants = event.participants

        return rec_event

    def get_events_in_interval(self, user_id: int, from_time: datetime, to_time: datetime = None) -> List[Union[Event, Invite]]:
        """
        Находит все встречи и инвайты пользователя в заданном интервале.
        """

        self.result = []
        events = self.filter_events(user_id, to_time=to_time)

        for event, meta, invite in events:
            if not event.is_recurrent and (event.starts_at >= from_time or (event.starts_at < from_time and event.ends_at > from_time)):
                self.add_to_result(user_id, event, invite)
            elif event.is_recurrent:
                start_time = meta.first_occurrence
                length_of_meeting = event.ends_at - event.starts_at
                end_time = start_time + length_of_meeting

                if to_time > start_time >= from_time:
                    self.add_to_result(user_id, event, invite)

                while start_time < to_time:
                    if meta.daily:
                        start_time += timedelta(days=meta.interval)
                        end_time = start_time + length_of_meeting
                    elif meta.yearly:
                        start_time += relativedelta(years=meta.interval)
                        end_time = start_time + length_of_meeting
                    elif meta.weekly:
                        start_time += timedelta(weeks=meta.interval)
                        end_time = start_time + length_of_meeting
                    elif meta.monthly:
                        start_time += relativedelta(months=meta.interval)
                        end_time = start_time + length_of_meeting

                    if from_time <= start_time < to_time:
                        rec_event = self.copy_event(event)
                        rec_event.starts_at = start_time
                        rec_event.ends_at = end_time

                        self.add_to_result(user_id, rec_event, invite)

        return self.result
