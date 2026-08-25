
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import api_error
from app.database.models.users import User
from app.database.models.department import Department
from app.database.models.employee import Employee, RoleName
from app.database.models.family_member import FamilyMember
from app.schema.auth import RegisterRequest
from app.utility.custom_id import generate_employee_id

def register_employee(data: RegisterRequest, db: Session) -> Employee:

    employee_data = data.employee
    department_ids = employee_data.department_ids

    if not department_ids:
        raise api_error(
            status_code=400,
            code="ATLEAST_ONE_DEPARTMENT_IS_NEED",
            message="employee should have atleast one department while registing",
        )

    departments = db.scalars(
        select(Department).where(Department.id.in_(department_ids))
    ).all()

    if len(departments) != len(set(department_ids)):
        raise api_error(
            status_code=400,
            code="INVALID_DEPARTMENT_ID",
            message="One or more department IDs are invalid",
        )


    employee = Employee(
        employee_id= None,
        interview_date=employee_data.interview_date,
        role=employee_data.role,

        # Personal details
        first_name=employee_data.first_name,
        middle_name=employee_data.middle_name,
        last_name=employee_data.last_name,
        gender=employee_data.gender,

        contact_no=employee_data.contact_no,
        alt_contact_no=employee_data.alt_contact_no,
        date_of_birth=employee_data.date_of_birth,

        pan=employee_data.pan,
        aadhar=employee_data.aadhar,

        current_address=employee_data.current_address,
        permanent_address=employee_data.permanent_address,

        # Bank details
        bank_name=employee_data.bank_name,
        bank_account_no=employee_data.bank_account_no,
        bank_ifsc=employee_data.bank_ifsc,

        # Qualification & experience
        qualifications=employee_data.qualifications,
        passout_year=employee_data.passout_year,
        experience_years=employee_data.experience_years,
        last_salary=employee_data.last_salary,
        skills=employee_data.skills,

        # Job details
        designation=employee_data.designation,
        location=employee_data.location,
        date_of_joining=employee_data.date_of_joining,
        date_of_leaving=employee_data.date_of_leaving,

        # Status
        is_active=employee_data.is_active,
        is_tms_user=employee_data.is_tms_user,
    )

    employee.departments = departments

    # Add family members
    for family_data in employee_data.family_members:
        family_member = FamilyMember(
            member_name=family_data.member_name,
            relation=family_data.relation,
            date_of_birth=family_data.date_of_birth,
            age=family_data.age,
            occupation=family_data.occupation,
        )

        employee.family_members.append(family_member)

    return employee

def update_employee_id(user: User, db: Session) -> None:
    user.employee.employee_id = generate_employee_id(user)
    db.commit()
