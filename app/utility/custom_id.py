from datetime import date

from app.core.errors import api_error
from app.database.models.users import User

def generate_employee_id(user: User) -> str:
    employee = user.employee

    if not employee.departments:
        raise api_error(
            status_code=400,
            code="NO_DEPARTMENT",
            message="Cannot generate employee ID without a department",
        )

    dept_code = employee.departments[0].name[:3].upper()
    join_date = employee.date_of_joining or date.today()
    mmyy = join_date.strftime("%m%y")
    id_tail = str(user.id).zfill(4)[-4:]

    return f"LA{dept_code}{mmyy}{id_tail}"