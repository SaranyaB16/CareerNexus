from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Student, CompanyDrive
from backend.schemas import DiagnosticRequest
from backend.services.criteria_engine import evaluate_eligibility_and_gaps

router = APIRouter(prefix="/api/diagnostics", tags=["Diagnostics"])


@router.post("/check-eligibility")
def run_eligibility_check(payload: DiagnosticRequest, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == payload.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    drive = db.query(CompanyDrive).filter(CompanyDrive.id == payload.company_id).first()
    if not drive:
        raise HTTPException(status_code=404, detail="Company drive not found")

    result = evaluate_eligibility_and_gaps(student, drive, db)
    return {
        "student": {
            "id": student.id,
            "name": student.name,
            "roll_no": student.roll_no,
            "cgpa": student.cgpa,
            "department": student.department,
            "backlogs": student.active_backlogs
        },
        "target_drive": {
            "id": drive.id,
            "company_name": drive.company_name,
            "role_title": drive.role_title,
            "tier": drive.tier,
            "ctc_lpa": drive.ctc_lpa,
            "min_cgpa": drive.min_cgpa
        },
        "diagnosis": result
    }
