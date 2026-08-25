from enum import Enum

from sqlalchemy import Column, Integer, String, CheckConstraint
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.core.database import Base


class UserType(str, Enum):
    MAIN_ADMIN = "main_admin"
    EMPLOYEE = "employee"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)

    user_type = Column(
        SQLEnum(UserType),
        nullable=False,
    )

    main_admin = relationship(
        "MainAdmin",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )

    employee = relationship(
        "Employee",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )