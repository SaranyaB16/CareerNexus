from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from backend.database import get_db
from backend.models import Application, Student, CompanyDrive
from backend.schemas import ApplicationOut, ApplicationCreate

router = APIRouter(prefix="/api/applications", tags=["Applications"])


class StageUpdateRequest(BaseModel):
    stage: str  # Applied, Online Assessment, Technical Round, HR Round, Offered, Rejected
    notes: str = ""


@router.get("/student/{student_id}")
def get_student_applications(student_id: int, db: Session = Depends(get_db)):
    apps = db.query(Application).filter(Application.student_id == student_id).all()
    results = []
    for a in apps:
        drive = db.query(CompanyDrive).filter(CompanyDrive.id == a.drive_id).first()
        results.append({
            "id": a.id,
            "student_id": a.student_id,
            "drive_id": a.drive_id,
            "company_name": drive.company_name if drive else "Unknown",
            "role_title": drive.role_title if drive else "Unknown",
            "ctc_lpa": drive.ctc_lpa if drive else 0.0,
            "tier": drive.tier if drive else "Standard",
            "stage": a.stage,
            "interview_date": a.interview_date,
            "notes": a.notes,
            "ai_match_score": a.ai_match_score,
            "is_reverse_pitch": a.is_reverse_pitch
        })
    return results


@router.post("", response_model=ApplicationOut)
def create_application(payload: ApplicationCreate, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == payload.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    drive = db.query(CompanyDrive).filter(CompanyDrive.id == payload.drive_id).first()
    if not drive:
        raise HTTPException(status_code=404, detail="Company drive not found")

    existing = db.query(Application).filter(
        Application.student_id == payload.student_id,
        Application.drive_id == payload.drive_id
    ).first()
    if existing:
        return existing

    app = Application(
        student_id=payload.student_id,
        drive_id=payload.drive_id,
        stage=payload.stage,
        notes=payload.notes or "",
        ai_match_score=85
    )
    db.add(app)
    db.commit()
    db.refresh(app)
    return app


@router.patch("/{application_id}/stage")
def update_stage(application_id: int, payload: StageUpdateRequest, db: Session = Depends(get_db)):
    app = db.query(Application).filter(Application.id == application_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")

    app.stage = payload.stage
    if payload.notes:
        app.notes = payload.notes

    # If offered, update student placement status
    if payload.stage == "Offered":
        student = db.query(Student).filter(Student.id == app.student_id).first()
        if student:
            student.placement_status = "Offered"

    db.commit()
    db.refresh(app)
    return {"status": "success", "application_id": app.id, "new_stage": app.stage}
