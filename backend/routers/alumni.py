from typing import List, Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Student, Alumni
from backend.schemas import AlumniOut, AlumniMatchRequest
from backend.services.alumni_service import match_alumni_for_student

router = APIRouter(prefix="/api/alumni", tags=["Alumni Bridge"])


class SessionBookingRequest(BaseModel):
    student_id: int
    alumni_id: int
    session_type: str = "15-Min Prep Call"  # 15-Min Prep Call or Warm Referral Request
    message: Optional[str] = "Looking for guidance on clearing the technical rounds."


@router.get("", response_model=List[AlumniOut])
def get_all_alumni(db: Session = Depends(get_db)):
    return db.query(Alumni).all()


@router.post("/match")
def match_alumni(payload: AlumniMatchRequest, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == payload.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    matches = match_alumni_for_student(student, db, payload.target_company)
    return {
        "student_name": student.name,
        "target_company": payload.target_company or student.target_company,
        "matched_count": len(matches),
        "alumni": matches
    }


@router.post("/request-session")
def request_alumni_session(payload: SessionBookingRequest, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == payload.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    alum = db.query(Alumni).filter(Alumni.id == payload.alumni_id).first()
    if not alum:
        raise HTTPException(status_code=404, detail="Alumni record not found")

    return {
        "status": "confirmed",
        "booking_id": f"ALUM-{student.id}-{alum.id}",
        "session_type": payload.session_type,
        "student_name": student.name,
        "alumni_name": alum.name,
        "alumni_company": alum.current_company,
        "alumni_email": alum.email,
        "calendar_invite": f"Google Meet link dispatched to {student.email} and {alum.email}",
        "message": f"Successfully connected with {alum.name} ({alum.current_role} at {alum.current_company})!"
    }
