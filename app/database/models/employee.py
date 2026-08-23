from enum import Enum

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.crypto import EncryptedString


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class RoleName(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    EMPLOYEE = "employee"
    USER = "user"


class Employee(Base):
    __tablename__ = "employees"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)

    employee_id = Column(String, unique=True, index=True, nullable=True)
    interview_date = Column(DateTime, nullable=True)

    role = Column(SQLEnum(RoleName), nullable=False, default=RoleName.EMPLOYEE)

    # Personal details
    first_name = Column(String(255), nullable=False)
    middle_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=False)
    gender = Column(SQLEnum(Gender), nullable=True)

    contact_no = Column(String(15), nullable=True)
    alt_contact_no = Column(String(15), nullable=True)
    date_of_birth = Column(Date, nullable=True)

    pan = Column(EncryptedString, nullable=True)
    aadhar = Column(EncryptedString, nullable=True)

    current_address = Column(Text, nullable=True)
    permanent_address = Column(Text, nullable=True)

    # Bank details
    bank_name = Column(EncryptedString, nullable=True)
    bank_account_no = Column(EncryptedString, nullable=True)
    bank_ifsc = Column(EncryptedString, nullable=True)

    # Qualification & experience
    qualifications = Column(ARRAY(String), nullable=True)
    passout_year = Column(Integer, nullable=True)
    experience_years = Column(Numeric(5, 2), nullable=True)
    last_salary = Column(Numeric(12, 2), nullable=True)
    skills = Column(ARRAY(String), nullable=True)

    # Job details
    designation = Column(String(100), nullable=True)
    location = Column(String(100), nullable=True)
    date_of_joining = Column(Date, nullable=True)
    date_of_leaving = Column(Date, nullable=True)

    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    is_tms_user = Column(Boolean, default=False, nullable=False)

    # Relationships
    user = relationship("User", back_populates="employee")

    family_members = relationship(
        "FamilyMember",
        back_populates="employee",
        cascade="all, delete-orphan",
    )

    departments = relationship(
        "Department",
        secondary=employee_departments,
        back_populates="employees",
    )