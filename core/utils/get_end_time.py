from typing import Union
from datetime import datetime

from core.models import Event, Invite


def get_end_time(item: Union[Event, Invite]) -> datetime:
    """
    Возвращает время конца встречи.
    """

    if isinstance(item, Event):
        return item.ends_at
    elif isinstance(item, Invite):
        return item.event.ends_at
