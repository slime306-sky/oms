from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


# --------------------------------------------------
# Employee <-> Department association table
# --------------------------------------------------

employee_departments = Table(
    "employee_departments",
    Base.metadata,
    Column("employee_user_id", Integer, ForeignKey(     "employees.user_id",     ondelete="CASCADE", ), primary_key=True),
    Column("department_id", Integer, ForeignKey(     "departments.id",     ondelete="CASCADE", ), primary_key=True),
)


# --------------------------------------------------
# Department
# --------------------------------------------------

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)

    # Department <-> Employee
    employees = relationship("Employee", secondary=employee_departments, back_populates="departments")