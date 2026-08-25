from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class FamilyMember(Base):
    __tablename__ = "family_members"

    id = Column(Integer, primary_key=True, index=True)
    employee_user_id = Column(
        Integer,
        ForeignKey("employees.user_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    member_name = Column(String(150), nullable=True)
    relation = Column(String(50), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    age = Column(Integer, nullable=True)
    occupation = Column(String(100), nullable=True)

    employee = relationship("Employee", back_populates="family_members")

    def __repr__(self):
        return f"<FamilyMember id={self.id} employee_user_id={self.employee_user_id} member_name={self.member_name!r}>"