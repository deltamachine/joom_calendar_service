from typing import List, Union
from datetime import datetime, timedelta

from core.services import IntervalService
from core.models import Event, Invite
from core.utils import get_start_time, get_end_time


class FreeSpotService:
    """
    Сервис для поиска свободных интервалов в календарях пользователей.
    """

    def __init__(self, db):
        self.db = db
        self.interval_service = IntervalService(db)

    def prepare_response(self, start_time: datetime, end_time: datetime) -> dict:
        """
        Оформляет ответ сервиса.
        """

        response = {
            "starts_at": start_time,
            "ends_at": end_time
        }

        return response

    def prepare_events(self, users: List[int], now: datetime) -> List[Union[Event, Invite]]:
        """
        Достает все встречи и приглашения для заданных пользователей начиная с заданного времени.
        """

        table = []

        for user in users:
            events = self.interval_service.get_events_in_interval(user, now)
            table += events

        table = sorted(table, key=lambda x: get_start_time(x))

        return table

    def get_closest_free_spot(self, users: List[int], meeting_length: int) -> dict:
        """
        Ищет ближайший свободный промежуток заданной длины для заданных пользователей.
        """

        delta = timedelta(minutes=meeting_length)
        now = datetime.now()

        table = self.prepare_events(users, now)

        prev_end = datetime.now()
        cur_start = get_start_time(table[0])

        if cur_start - prev_end >= delta:
            return self.prepare_response(prev_end, prev_end + delta)

        for i in range(1, len(table)):
            prev_end = get_end_time(table[i-1])
            cur_start = get_start_time(table[i])

            if cur_start - prev_end >= delta:
                return self.prepare_response(prev_end, prev_end + delta)

        prev_end = get_end_time(table[i])

        return self.prepare_response(prev_end, prev_end + delta)
