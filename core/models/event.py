from sqlalchemy import Table, Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from core.db import Base


association_table = Table(
    "association",
    Base.metadata,
    Column("event_id", ForeignKey("event.id")),
    Column("user_id", ForeignKey("user.id")),
)


class Event(Base):
    """
    Модель для хранения информации о событии в календаре.
    """

    __tablename__ = "event"

    id = Column(Integer, primary_key=True, index=True)
    starts_at = Column(DateTime)
    ends_at = Column(DateTime)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", backref="Event")
    participants = relationship("User", secondary=association_table)
    description = Column(String(1000), nullable=True)
    is_private = Column(Boolean, default=False)
    is_recurrent = Column(Boolean, default=False)
    recurrency_rule = Column(String(100), nullable=True)

    def __str__(self):
        return f"Event {self.id}"
