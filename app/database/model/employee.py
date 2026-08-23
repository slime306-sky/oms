from sqlalchemy import CheckConstraint, Column, Integer, String, Enum as SQLEnum
from sqlalchemy.orm import relationship

from enum import Enum

from app.core.database import Base

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class RoleName(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    EMPLOYEE = "employee"
    USER = "user"

class User(Base):
    __tablename__ = "users"
    __table_args__ = (CheckConstraint("password <> ''", name="ck_users_password_not_empty"),)

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(String, unique=True, index=True) 
    interview_date = Column(DateTime, nullable=True) 

    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(SQLEnum(RoleName), nullable=False, default=RoleName.EMPLOYEE)
    
    
    first_name = Column(String(255), nullable=False)
    middle_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    
    gender = Column(SQLEnum(Gender), nullable=True)

    contact_no = Column(String(20), nullable=True)

    date_of_birth = Column(Date, nullable=True)
    pan = Column(String, nullable=True)
    aadhar = Column(String, nullable=True)
    contact_no = Column(String(15), nullable=True)
    alt_contact_no = Column(String(15), nullable=True)
    current_address = Column(Text, nullable=True)
    permanent_address = Column(Text, nullable=True)

    # --- Bank details ---
    bank_name = Column(String(150), nullable=True)
    bank_account_no = Column(String, nullable=True)
    bank_ifsc = Column(String, nullable=True)
 
    # --- Qualification & experience ---
    qualifications = Column(ARRAY(String), nullable=True)  
    passout_year = Column(Integer, nullable=True)
    experience_years = Column(Numeric(5, 2), nullable=True)
    last_salary = Column(Numeric(12, 2), nullable=True)
    skills = Column(ARRAY(String), nullable=True)
 
    # --- Job details ---
    department = Column(String(100), nullable=True)
    designation = Column(String(100), nullable=True)
    location = Column(String(100), nullable=True)
    date_of_joining = Column(Date, nullable=True)
    date_of_leaving = Column(Date, nullable=True)
    
    is_active = Column(Boolean, default=True, nullable=False)
    is_tms_user = Column(Boolean, default=False, nullable=False)

    # --- Relationships ---

    family_members = relationship(
        "FamilyMember",
        back_populates="user",
        cascade="all, delete-orphan",
    )
 
    departments = relationship(
        "Department",
        secondary=user_departments,
        back_populates="users",
    )