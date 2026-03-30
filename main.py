from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from database import get_session, create_db_and_tables
from models import Student, Department
from passlib.context import CryptContext
from typing import List

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Enable CORS so Frontend can talk to Backend
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# --- AUTHENTICATION ---
@app.post("/register")
def register(student: Student, session: Session = Depends(get_session)):
    # Hash the password before saving
    student.password = pwd_context.hash(student.password)
    session.add(student)
    session.commit()
    return {"message": "User registered successfully"}

@app.post("/login")
def login(data: dict, session: Session = Depends(get_session)):
    statement = select(Student).where(Student.email == data["email"])
    user = session.exec(statement).first()
    if not user or not pwd_context.verify(data["password"], user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"message": "Login successful", "is_admin": user.is_admin, "user_id": user.student_id}

# --- CRUD OPERATIONS (ADMIN ONLY LOGIC) ---
@app.get("/students", response_model=List[Student])
def get_all_students(session: Session = Depends(get_session)):
    return session.exec(select(Student)).all()

@app.put("/students/{id}")
def update_student(id: int, updated_data: Student, session: Session = Depends(get_session)):
    db_student = session.get(Student, id)
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student_data = updated_data.dict(exclude_unset=True)
    for key, value in student_data.items():
        setattr(db_student, key, value)
    
    session.add(db_student)
    session.commit()
    return {"message": "Updated"}

@app.delete("/students/{id}")
def delete_student(id: int, session: Session = Depends(get_session)):
    db_student = session.get(Student, id)
    session.delete(db_student)
    session.commit()
    return {"message": "Deleted"}