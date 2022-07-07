from typing import List, Optional
from datetime import datetime

from fastapi import HTTPException
from pydantic import BaseModel, validator


class EventCreateRequest(BaseModel):
    """
    Схема, валидирующая запрос о создании события.
    """

    starts_at: datetime
    ends_at: datetime
    owner_id: int
    participants: Optional[List[int]]
    description: Optional[str]
    is_private: bool
    is_recurrent: bool
    recurrency_rule: Optional[str]

    @validator("starts_at", "ends_at", pre=True)
    def str_to_datetime(cls, value: str) -> datetime:
        return datetime.strptime(value, "%Y-%m-%d %H:%M")

    @validator("recurrency_rule")
    def check_recurrency_rule(cls, value: str) -> str:
        rule = value.split(' | ')

        if len(rule) != 4:
            raise HTTPException(
                status_code=400,
                detail="Неправильно задан формат правила повторения")

        freq = rule[0]
        details = rule[1]
        interval = rule[3]

        if (freq == 'yearly' or freq == 'daily' or freq ==
                'monthly') and bool(details) is True:
            return value
        elif freq == 'weekly':
            try:
                [int(x) for x in details.split(', ')]
                return value
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="Неправильно задан формат правила повторения")

        try:
            int(interval)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Неправильно задан формат правила повторения")

        raise HTTPException(
            status_code=400,
            detail="Неправильно задан формат правила повторения")
