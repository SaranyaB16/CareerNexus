from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Student, CompanyDrive
from backend.schemas import StudentOut, StudentCreate

router = APIRouter(prefix="/api/students", tags=["Students"])


@router.get("", response_model=List[StudentOut])
def get_students(db: Session = Depends(get_db)):
    return db.query(Student).all()


@router.get("/{student_id}", response_model=StudentOut)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.post("", response_model=StudentOut)
def create_student(payload: StudentCreate, db: Session = Depends(get_db)):
    existing = db.query(Student).filter(Student.roll_no == payload.roll_no).first()
    if existing:
        raise HTTPException(status_code=400, detail="Student with this roll number already exists")

    student = Student(**payload.model_dump())
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


@router.put("/{student_id}", response_model=StudentOut)
def update_student(student_id: int, payload: StudentCreate, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    for field, value in payload.model_dump().items():
        setattr(student, field, value)

    # Recalculate risk level
    if student.active_backlogs > 0 or student.cgpa < 6.5:
        student.risk_level = "At-Risk"
    elif student.cgpa < 7.5 or not student.verified_project_badge:
        student.risk_level = "Moderate"
    else:
        student.risk_level = "Safe"

    db.commit()
    db.refresh(student)
    return student
