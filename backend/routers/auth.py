import hashlib
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import User, Student

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


class SignupRequest(BaseModel):
    name: str
    email: str
    password: str
    role: str = "student"  # "student" or "recruiter"
    # Student specific fields
    roll_no: Optional[str] = None
    department: Optional[str] = "Computer Science"
    cgpa: Optional[float] = 7.5
    # Recruiter specific fields
    company: Optional[str] = None


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/signup")
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    # Check if user email already exists
    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="An account with this email already exists")

    student_id = None
    if payload.role.lower() == "student":
        # Create student profile
        roll = payload.roll_no or f"22{payload.department[:2].upper()}{100 + db.query(Student).count() + 1}"
        existing_student = db.query(Student).filter(Student.roll_no == roll).first()
        if existing_student:
            roll = f"{roll}-{db.query(Student).count() + 1}"

        new_student = Student(
            roll_no=roll,
            name=payload.name,
            email=payload.email,
            department=payload.department or "Computer Science",
            cgpa=payload.cgpa or 7.5,
            graduation_year=2026,
            active_backlogs=0,
            skills="Python, SQL, Problem Solving",
            target_role="Software Development Engineer",
            target_company="Amazon",
            risk_level="Safe" if (payload.cgpa or 7.5) >= 7.5 else "Moderate",
            placement_status="Unplaced"
        )
        db.add(new_student)
        db.commit()
        db.refresh(new_student)
        student_id = new_student.id

    # Create User account
    user = User(
        name=payload.name,
        email=payload.email,
        password_hash=hash_password(payload.password),
        role=payload.role.lower(),
        company=payload.company if payload.role.lower() == "recruiter" else "",
        student_id=student_id
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "status": "success",
        "message": f"Welcome to CareerNexus, {user.name}!",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "company": user.company,
            "student_id": user.student_id
        }
    }


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if user.password_hash != hash_password(payload.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {
        "status": "success",
        "message": f"Welcome back, {user.name}!",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "company": user.company,
            "student_id": user.student_id
        }
    }


@router.get("/demo-accounts")
def get_demo_accounts(db: Session = Depends(get_db)):
    """Returns sample pre-configured accounts for quick 1-click evaluation"""
    return [
        {
            "role": "student",
            "name": "Aarav Sharma",
            "email": "aarav.sharma@college.edu",
            "password": "password123",
            "description": "CSE Student (CGPA 8.8, Verified Projects)"
        },
        {
            "role": "student",
            "name": "Priya Patel",
            "email": "priya.patel@college.edu",
            "password": "password123",
            "description": "IT Student (CGPA 7.3, Gap Analysis Focus)"
        },
        {
            "role": "recruiter",
            "name": "Sarah Jenkins",
            "email": "recruiter@amazon.com",
            "password": "password123",
            "company": "Amazon",
            "description": "Technical Campus Recruiter @ Amazon"
        }
    ]
