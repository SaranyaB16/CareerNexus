from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from backend.models import Student, Alumni


def match_alumni_for_student(student: Student, db: Session, target_company: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Pairs students with campus alumni currently employed at their target dream companies.
    """
    target = (target_company or student.target_company or "").strip().lower()

    all_alumni = db.query(Alumni).all()
    results = []

    for alum in all_alumni:
        alum_company = alum.current_company.strip().lower()
        company_match = target in alum_company or alum_company in target
        dept_match = student.department.lower() == alum.department.lower()

        # Score affinity
        affinity_score = 50
        if company_match:
            affinity_score += 35
        if dept_match:
            affinity_score += 15

        reasons = []
        if company_match:
            reasons.append(f"Currently works at your target company: {alum.current_company}")
        if dept_match:
            reasons.append(f"Same department senior ({alum.department}, Class of {alum.graduation_batch})")

        results.append({
            "id": alum.id,
            "name": alum.name,
            "email": alum.email,
            "current_company": alum.current_company,
            "current_role": alum.current_role,
            "graduation_batch": alum.graduation_batch,
            "department": alum.department,
            "linkedin_url": alum.linkedin_url,
            "available_for_mock": alum.available_for_mock,
            "referral_status": alum.referral_status,
            "bio": alum.bio,
            "affinity_score": min(affinity_score, 100),
            "match_reasons": reasons or ["Experienced alumni mentor in technology sector"]
        })

    # Sort by affinity score descending
    results.sort(key=lambda x: x["affinity_score"], reverse=True)
    return results
