from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Student, CompanyDrive, Application
from backend.schemas import ReversePitchSearchRequest, ReversePitchInviteRequest

router = APIRouter(prefix="/api/recruiter", tags=["Recruiter Reverse Pitch"])


@router.post("/reverse-pitch/search")
def search_talent_pool(payload: ReversePitchSearchRequest, db: Session = Depends(get_db)):
    """
    Allows recruiters to search candidates matching custom criteria without waiting for students to apply.
    """
    query = db.query(Student)

    if payload.min_cgpa is not None:
        query = query.filter(Student.cgpa >= payload.min_cgpa)

    if payload.max_backlogs is not None:
        query = query.filter(Student.active_backlogs <= payload.max_backlogs)

    if payload.department:
        query = query.filter(Student.department.ilike(f"%{payload.department}%"))

    if payload.verified_project_only:
        query = query.filter(Student.verified_project_badge == True)

    students = query.all()

    # Filter by skills if provided
    matched_results = []
    for s in students:
        s_skills = [x.strip().lower() for x in s.skills.split(",") if x.strip()]
        if payload.skills:
            req_set = set([k.strip().lower() for k in payload.skills if k.strip()])
            common = req_set.intersection(set(s_skills))
            if not common:
                continue
            skill_score = int((len(common) / len(req_set)) * 100)
        else:
            skill_score = 90

        matched_results.append({
            "id": s.id,
            "roll_no": s.roll_no,
            "name": s.name,
            "department": s.department,
            "cgpa": s.cgpa,
            "backlogs": s.active_backlogs,
            "skills": s.skills,
            "github_username": s.github_username,
            "github_proof_score": s.github_proof_score,
            "verified_project_badge": s.verified_project_badge,
            "risk_level": s.risk_level,
            "placement_status": s.placement_status,
            "skill_match_percentage": skill_score
        })

    # Sort candidates with verified projects and higher CGPAs first
    matched_results.sort(key=lambda x: (x["verified_project_badge"], x["cgpa"]), reverse=True)

    return {
        "total_matches": len(matched_results),
        "candidates": matched_results
    }


@router.post("/reverse-pitch/invite")
def send_fast_track_invites(payload: ReversePitchInviteRequest, db: Session = Depends(get_db)):
    """
    Sends direct Fast-Track Interview invites from recruiters to selected students.
    """
    drive = db.query(CompanyDrive).filter(CompanyDrive.id == payload.drive_id).first()
    if not drive:
        raise HTTPException(status_code=404, detail="Company drive not found")

    created_invites = []
    for sid in payload.student_ids:
        student = db.query(Student).filter(Student.id == sid).first()
        if not student:
            continue

        # Check if already invited or applied
        existing = db.query(Application).filter(
            Application.student_id == sid,
            Application.drive_id == payload.drive_id
        ).first()

        if existing:
            existing.stage = "Online Assessment"
            existing.is_reverse_pitch = True
            existing.notes = payload.custom_message or "Fast-tracked by recruiter via Reverse Pitch."
            created_invites.append(existing.id)
        else:
            app = Application(
                student_id=sid,
                drive_id=payload.drive_id,
                stage="Online Assessment",
                is_reverse_pitch=True,
                notes=payload.custom_message or f"Fast-Track Invite sent by {drive.company_name} recruiter."
            )
            db.add(app)
            student.placement_status = "Shortlisted"
            db.commit()
            db.refresh(app)
            created_invites.append(app.id)

    return {
        "status": "success",
        "company": drive.company_name,
        "role": drive.role_title,
        "invited_count": len(created_invites),
        "application_ids": created_invites,
        "message": f"Successfully sent Fast-Track interview invites to {len(created_invites)} candidate(s)!"
    }
