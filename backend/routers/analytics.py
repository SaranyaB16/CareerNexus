from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Student, CompanyDrive, RemediationCohort

router = APIRouter(prefix="/api/analytics", tags=["TPO Analytics"])


@router.get("/tpo-dashboard")
def get_tpo_analytics(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    drives = db.query(CompanyDrive).all()
    cohorts = db.query(RemediationCohort).all()

    total_students = len(students)
    placed_students = [s for s in students if s.placement_status in ["Placed", "Offered"]]
    at_risk_students = [s for s in students if s.risk_level == "At-Risk"]
    moderate_students = [s for s in students if s.risk_level == "Moderate"]
    safe_students = [s for s in students if s.risk_level == "Safe"]

    # Calculate CTC statistics from drives
    ctcs = [d.ctc_lpa for d in drives]
    avg_ctc = round(sum(ctcs) / max(len(ctcs), 1), 1)
    max_ctc = max(ctcs) if ctcs else 0.0

    # Department breakdown
    dept_stats = {}
    for s in students:
        dept = s.department
        if dept not in dept_stats:
            dept_stats[dept] = {"total": 0, "placed": 0}
        dept_stats[dept]["total"] += 1
        if s.placement_status in ["Placed", "Offered"]:
            dept_stats[dept]["placed"] += 1

    return {
        "kpis": {
            "total_students": total_students,
            "placement_rate_pct": round((len(placed_students) / max(total_students, 1)) * 100, 1),
            "average_ctc_lpa": avg_ctc,
            "highest_ctc_lpa": max_ctc,
            "active_drives_count": len(drives),
            "at_risk_students_count": len(at_risk_students)
        },
        "risk_breakdown": {
            "safe": len(safe_students),
            "moderate": len(moderate_students),
            "at_risk": len(at_risk_students)
        },
        "at_risk_students": [
            {
                "id": s.id,
                "roll_no": s.roll_no,
                "name": s.name,
                "department": s.department,
                "cgpa": s.cgpa,
                "backlogs": s.active_backlogs,
                "risk_level": s.risk_level,
                "suggested_cohort": "DSA Accelerator" if s.cgpa < 6.5 else "Aptitude Sprint"
            }
            for s in at_risk_students
        ],
        "department_placement": dept_stats,
        "active_cohorts": [
            {
                "id": c.id,
                "name": c.name,
                "category": c.category,
                "mentor": c.mentor,
                "weekly_task": c.weekly_task
            }
            for c in cohorts
        ]
    }
