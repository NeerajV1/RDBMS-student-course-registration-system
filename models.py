from typing import Optional
from datetime import date
from sqlmodel import SQLModel, Field

# 1. Department Table
class Department(SQLModel, table=True):
    dept_id: Optional[int] = Field(default=None, primary_key=True)
    dept_name: str
    location: str

# 2. Student Table (Matches your ER Diagram)
class Student(SQLModel, table=True):
    student_id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    phoneno: str
    dob: date
    semester: int
    password: str  # For Login
    is_admin: bool = False
    dept_id: Optional[int] = Field(default=None, foreign_key="department.dept_id")

# 3. Course Table
class Course(SQLModel, table=True):
    course_id: Optional[int] = Field(default=None, primary_key=True)
    course_name: str
    course_duration: str
    credit: int