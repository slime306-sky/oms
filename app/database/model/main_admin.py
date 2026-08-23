from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class MainAdmin(Base):
    __tablename__ = "main_admins"

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )

    user = relationship(
        "User",
        back_populates="main_admin",
    )