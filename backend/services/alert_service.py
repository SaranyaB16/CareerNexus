from typing import List, Dict, Any
from sqlalchemy.orm import Session
from backend.models import Student, CompanyDrive, PlacementAlert


def generate_smart_alerts_for_student(student: Student, db: Session) -> List[Dict[str, Any]]:
    """
    Evaluates active campus drives and generates personalized, priority-ranked alerts.
    """
    alerts = []
    drives = db.query(CompanyDrive).filter(CompanyDrive.status == "Open").all()

    student_skills = set([s.strip().lower() for s in student.skills.split(",") if s.strip()])

    for drive in drives:
        drive_skills = [s.strip().lower() for s in drive.required_skills.split(",") if s.strip()]
        matched = [s for s in drive_skills if s in student_skills]
        match_pct = int((len(matched) / max(len(drive_skills), 1)) * 100)

        # 1. High match alert
        if match_pct >= 75 and student.cgpa >= drive.min_cgpa and student.active_backlogs <= drive.max_backlogs:
            alerts.append({
                "title": f"🎯 {match_pct}% Match: {drive.company_name} Drive Opened",
                "message": f"{drive.company_name} is hiring for {drive.role_title} ({drive.ctc_lpa} LPA). Your profile is a top match for their required tech stack.",
                "alert_type": "match",
                "urgency": "high",
                "drive_id": drive.id,
                "company_name": drive.company_name
            })
        
        # 2. Urgent deadline alert
        if drive.deadline:
            alerts.append({
                "title": f"⏰ Deadline Approaching: {drive.company_name}",
                "message": f"Registration for {drive.company_name} ({drive.role_title}) closes on {drive.deadline}. Verify your resume before submission.",
                "alert_type": "deadline",
                "urgency": "high",
                "drive_id": drive.id,
                "company_name": drive.company_name
            })

    # 3. Eligibility unlock notification if student has good CGPA
    if student.cgpa >= 8.5:
        alerts.append({
            "title": "🌟 Super Dream Tier Unlocked",
            "message": f"With your current CGPA of {student.cgpa}, you are eligible for elite Super Dream tier companies (>15 LPA) with priority interview slots.",
            "alert_type": "unlock",
            "urgency": "info",
            "drive_id": None,
            "company_name": "Campus Placement Cell"
        })

    # 4. Proof of work badge alert
    if student.verified_project_badge:
        alerts.append({
            "title": "🛡️ Verified Project Badge Active",
            "message": "Your GitHub portfolio is verified! Your profile is now boosted to top recruiter search rankings.",
            "alert_type": "unlock",
            "urgency": "info",
            "drive_id": None,
            "company_name": "CampusPulse System"
        })

    return alerts
