from typing import Union
from datetime import datetime

from core.models import Event, Invite


def get_start_time(item: Union[Event, Invite]) -> datetime:
    """
    Возвращает время начала встречи.
    """

    if isinstance(item, Event):
        return item.starts_at
    elif isinstance(item, Invite):
        return item.event.starts_at
