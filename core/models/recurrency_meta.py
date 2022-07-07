from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from core.db import Base


class RecurrencyMeta(Base):
    """
    Модель для хранения информации о повторяемости события в календаре.
    """

    __tablename__ = "recurrency_meta"

    id = Column(Integer, primary_key=True, index=True)
    first_occurrence = Column(DateTime)
    last_occurrence = Column(DateTime, nullable=True)
    event_id = Column(Integer, ForeignKey("event.id"))
    event = relationship("Event", backref="RecurrencyMeta")
    daily = Column(Boolean, default=False)
    yearly = Column(Boolean, default=False)
    weekly = Column(Boolean, default=False)
    monthly = Column(Boolean, default=False)
    interval = Column(Integer, default=1)

    def __str__(self):
        return f"Recurrency meta: {self.id}, event {self.event_id}"
