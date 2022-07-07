from typing import List
from datetime import timedelta

from core.models import RecurrencyMeta, Event


class RecurrencyMetaService:
    """
    Сервис для работы с таблицей RecurrencyMeta.
    """

    def __init__(self, db):
        self.db = db

    def parse_recurrency_rule(self, rule: str) -> dict:
        """
        Парсит переданное правило повторения.
        """

        rule = rule.split(' | ')
        freq = rule[0]
        details = rule[1]
        interval = int(rule[3])

        if freq == 'yearly' or freq == 'daily':
            return {freq: bool(details)}
        elif freq == 'monthly':
            return {freq: details}
        elif freq == 'weekly':
            return {
                freq: [
                    int(x) for x in details.split(', ')],
                'interval': interval}

    def create_recurrency_meta(self, event: Event) -> List[RecurrencyMeta]:
        """
        Создает правила повторения для заданной встречи.
        """

        rule = self.parse_recurrency_rule(event.recurrency_rule)

        metas = []

        if not rule.get("weekly"):
            meta = RecurrencyMeta()
            meta.event_id = event.id
            meta.first_occurrence = event.starts_at
            meta.interval = rule.get('interval')

            if rule.get('daily'):
                meta.daily = True
            elif rule.get('yearly'):
                meta.yearly = True
            elif rule.get('monthly'):
                meta.monthly = True

            metas.append(meta)
        elif rule.get('weekly'):
            days = rule.get('weekly')

            day_of_week = event.starts_at.weekday()

            for day in days:
                meta = RecurrencyMeta()
                meta.event_id = event.id
                meta.weekly = True
                meta.interval = rule.get('interval')

                if day == day_of_week:
                    meta.first_occurrence = event.starts_at
                elif day > day_of_week:
                    delta = day - day_of_week
                    meta.first_occurrence = event.starts_at + \
                        timedelta(days=delta)
                else:
                    delta = day + (day_of_week - day) + 1
                    meta.first_occurrence = event.starts_at + \
                        timedelta(days=delta)

                metas.append(meta)

        return metas

    def insert_many_recurrency_meta(self, metas: List[RecurrencyMeta]) -> None:
        """
        Добавляет несколько записей о повторениях встреч в базу данных.
        """

        self.db.bulk_save_objects(metas)
        self.db.commit()
