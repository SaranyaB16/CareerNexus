from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Student
from backend.schemas import GitHubAuditRequest
from backend.services.github_service import audit_github_profile

router = APIRouter(prefix="/api/github", tags=["GitHub Validator"])


@router.post("/audit")
def audit_profile(payload: GitHubAuditRequest, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == payload.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    audit_result = audit_github_profile(
        username=payload.github_username or student.github_username or "candidate",
        sample_repo=payload.sample_repo_url
    )

    # Persist score and badge in student profile
    student.github_username = payload.github_username or student.github_username
    student.github_proof_score = audit_result["proof_of_work_score"]
    student.verified_project_badge = audit_result["verified_project_badge"]

    # Re-evaluate risk level
    if student.active_backlogs == 0 and student.cgpa >= 7.5 and student.verified_project_badge:
        student.risk_level = "Safe"
    elif student.active_backlogs > 0 or student.cgpa < 6.5:
        student.risk_level = "At-Risk"
    else:
        student.risk_level = "Moderate"

    db.commit()
    db.refresh(student)

    return {
        "student_id": student.id,
        "student_name": student.name,
        "audit": audit_result
    }
