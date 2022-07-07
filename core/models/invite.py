from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from core.db import Base


class Invite(Base):
    """
    Модель для хранения приглашения на встречу в календаре.
    """

    __tablename__ = "invite"

    id = Column(Integer, primary_key=True, index=True)
    invitee_id = Column(Integer, ForeignKey("user.id"))
    invitee = relationship("User", backref="invite")
    event_id = Column(Integer, ForeignKey("event.id"))
    event = relationship("Event", backref="invite")
    is_accepted = Column(Boolean, default=False)
    is_viewed = Column(Boolean, default=False)

    def __str__(self):
        return f"Invite {self.id}"
