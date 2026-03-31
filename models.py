from typing import Optional, List
from datetime import date
from sqlmodel import SQLModel, Field, Relationship

class Department(SQLModel, table=True):
    dept_id: Optional[int] = Field(default=None, primary_key=True)
    dept_name: str = Field(index=True)
    location: str

    students: List["Student"] = Relationship(back_populates="department")
    teachers: List["Teacher"] = Relationship(back_populates="department")

class Course(SQLModel, table=True):
    course_id: Optional[int] = Field(default=None, primary_key=True)
    course_name: str
    course_duration: str
    credit: int

class Teacher(SQLModel, table=True):
    teacher_id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True, index=True)
    dept_id: Optional[int] = Field(default=None, foreign_key="department.dept_id")
    
    department: Optional[Department] = Relationship(back_populates="teachers")

class Student(SQLModel, table=True):
    student_id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    phoneno: str
    dob: date
    semester: int
    password: str
    is_admin: bool = Field(default=False)
    dept_id: Optional[int] = Field(default=None, foreign_key="department.dept_id")
    
    department: Optional[Department] = Relationship(back_populates="students")