from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from database import get_session, create_db_and_tables
from models import Student, Department, Teacher, Course
from typing import List

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# --- CREATE OPERATIONS ---
@app.post("/students/")
def create_student(student: Student, session: Session = Depends(get_session)):
    session.add(student)
    session.commit()
    return {"message": "INSERT SUCCESS: Student added to database!"}

@app.post("/departments/")
def create_dept(dept: Department, session: Session = Depends(get_session)):
    session.add(dept)
    session.commit()
    return {"message": "INSERT SUCCESS: Department created!"}

# --- READ OPERATIONS ---
@app.get("/students/", response_model=List[Student])
def get_students(session: Session = Depends(get_session)):
    return session.exec(select(Student)).all()

@app.get("/departments/", response_model=List[Department])
def get_depts(session: Session = Depends(get_session)):
    return session.exec(select(Department)).all()

# --- DELETE OPERATIONS ---
@app.delete("/students/{id}")
def delete_student(id: int, session: Session = Depends(get_session)):
    student = session.get(Student, id)
    if not student:
        raise HTTPException(status_code=404, detail="Record not found")
    session.delete(student)
    session.commit()
    return {"message": f"DELETE SUCCESS: Record {id} removed!"}