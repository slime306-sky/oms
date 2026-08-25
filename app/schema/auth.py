from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field

from app.database.models.employee import Gender, RoleName
from app.database.models.users import UserType


class FamilyMemberCreate(BaseModel):
    member_name: Optional[str] = None
    relation: Optional[str] = None
    date_of_birth: Optional[date] = None
    age: Optional[int] = None
    occupation: Optional[str] = None


class EmployeeCreate(BaseModel):
    interview_date: Optional[datetime] = None
    role: RoleName = RoleName.EMPLOYEE

    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    gender: Optional[Gender] = None

    

    contact_no: Optional[str] = None
    alt_contact_no: Optional[str] = None
    date_of_birth: Optional[date] = None

    pan: Optional[str] = None
    aadhar: Optional[str] = None

    current_address: Optional[str] = None
    permanent_address: Optional[str] = None

    bank_name: Optional[str] = None
    bank_account_no: Optional[str] = None
    bank_ifsc: Optional[str] = None

    qualifications: Optional[List[str]] = None
    passout_year: Optional[int] = None
    experience_years: Optional[Decimal] = None
    last_salary: Optional[Decimal] = None
    skills: Optional[List[str]] = None

    designation: Optional[str] = None
    location: Optional[str] = None
    date_of_joining: Optional[date] = None
    date_of_leaving: Optional[date] = None

    is_active: bool = True
    is_tms_user: bool = False

    family_members: List[FamilyMemberCreate] = []
    department_ids: List[int] = Field(default_factory=list)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    user_type: UserType

    employee: Optional[EmployeeCreate] = None