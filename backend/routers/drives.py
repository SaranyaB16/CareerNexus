import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import CompanyDrive, DriveForensics
from backend.schemas import CompanyDriveOut

router = APIRouter(prefix="/api/drives", tags=["Drives"])


@router.get("", response_model=List[CompanyDriveOut])
def get_drives(status: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(CompanyDrive)
    if status:
        query = query.filter(CompanyDrive.status == status)
    return query.all()


@router.get("/{drive_id}", response_model=CompanyDriveOut)
def get_drive(drive_id: int, db: Session = Depends(get_db)):
    drive = db.query(CompanyDrive).filter(CompanyDrive.id == drive_id).first()
    if not drive:
        raise HTTPException(status_code=404, detail="Drive not found")
    return drive


@router.get("/{drive_id}/forensics")
def get_drive_forensics(drive_id: int, db: Session = Depends(get_db)):
    drive = db.query(CompanyDrive).filter(CompanyDrive.id == drive_id).first()
    if not drive:
        raise HTTPException(status_code=404, detail="Drive not found")

    forensics = db.query(DriveForensics).filter(
        DriveForensics.company_name.ilike(f"%{drive.company_name}%")
    ).first()

    if not forensics:
        # Default fallback forensics
        return {
            "company_name": drive.company_name,
            "role_title": drive.role_title,
            "ctc_lpa": drive.ctc_lpa,
            "selection_rate": 18.5,
            "frequent_topics": "Data Structures, System Design, REST APIs, Behavioral Questions",
            "rounds": [
                {"round": 1, "name": "Online Assessment", "duration": "90 mins", "focus": "2 Coding Problems (Arrays/Graphs) + 20 Aptitude Questions"},
                {"round": 2, "name": "Technical Interview 1", "duration": "45 mins", "focus": "Data Structures, Algorithm Optimization, Project Architecture"},
                {"round": 3, "name": "Technical Interview 2", "duration": "45 mins", "focus": "System Design, Database Concurrency, Code Quality"},
                {"round": 4, "name": "HR & Culture Fit", "duration": "30 mins", "focus": "Company Values, Leadership Principles, Scenario Questions"}
            ],
            "interview_tips": f"Focus on high code quality and clear trade-off explanations when interviewers ask about your projects for {drive.company_name}."
        }

    rounds = []
    try:
        rounds = json.loads(forensics.rounds_json)
    except Exception:
        rounds = []

    return {
        "company_name": drive.company_name,
        "role_title": drive.role_title,
        "ctc_lpa": drive.ctc_lpa,
        "selection_rate": forensics.selection_rate,
        "frequent_topics": forensics.frequent_topics,
        "rounds": rounds,
        "interview_tips": forensics.interview_tips
    }
