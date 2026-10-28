from typing import Dict, Any, List
from sqlalchemy.orm import Session
from backend.models import Student, CompanyDrive, LearningResource


def evaluate_eligibility_and_gaps(student: Student, drive: CompanyDrive, db: Session) -> Dict[str, Any]:
    """
    Evaluates student profile against company drive requirements.
    Detects missing criteria (CGPA, backlogs, branch, skills) and maps free learning resources.
    """
    gaps = []
    strengths = []
    is_eligible = True

    # 1. CGPA evaluation
    if student.cgpa < drive.min_cgpa:
        deficit = round(drive.min_cgpa - student.cgpa, 2)
        gaps.append({
            "type": "Academic",
            "category": "CGPA Deficit",
            "required": f"{drive.min_cgpa} CGPA",
            "current": f"{student.cgpa} CGPA",
            "severity": "High" if deficit >= 0.5 else "Medium",
            "remediation": f"Target +{deficit} CGPA in upcoming semester exams or submit strong portfolio waiver."
        })
        is_eligible = False
    else:
        strengths.append(f"Meets CGPA cutoff: {student.cgpa} >= {drive.min_cgpa}")

    # 2. Backlogs evaluation
    if student.active_backlogs > drive.max_backlogs:
        gaps.append({
            "type": "Academic",
            "category": "Active Backlogs",
            "required": f"Max {drive.max_backlogs} backlogs",
            "current": f"{student.active_backlogs} active backlog(s)",
            "severity": "Critical",
            "remediation": "Clear remedial exams before drive date to unlock registration."
        })
        is_eligible = False
    else:
        strengths.append("Zero backlog restriction passed")

    # 3. Department evaluation
    allowed_list = [b.strip().lower() for b in drive.allowed_branches.split(",")] if drive.allowed_branches != "All" else ["all"]
    if "all" not in allowed_list and student.department.strip().lower() not in allowed_list:
        gaps.append({
            "type": "Policy",
            "category": "Department Eligibility",
            "required": drive.allowed_branches,
            "current": student.department,
            "severity": "High",
            "remediation": "Request off-campus / open-category consideration from TPO placement officer."
        })
        is_eligible = False
    else:
        strengths.append(f"Eligible department: {student.department}")

    # 4. Technical Skills Gap
    student_skills_set = set([s.strip().lower() for s in student.skills.split(",") if s.strip()])
    required_skills_list = [s.strip() for s in drive.required_skills.split(",") if s.strip()]

    matched_skills = []
    missing_skills = []

    for req in required_skills_list:
        if req.lower() in student_skills_set:
            matched_skills.append(req)
        else:
            missing_skills.append(req)

    # Calculate match percentage
    if required_skills_list:
        skill_match_pct = int((len(matched_skills) / len(required_skills_list)) * 100)
    else:
        skill_match_pct = 80

    for missing in missing_skills:
        gaps.append({
            "type": "Technical Skill",
            "category": "Missing Core Skill",
            "required": missing,
            "current": "Not listed on profile",
            "severity": "Medium",
            "remediation": f"Master {missing} fundamentals using recommended curated resources below."
        })

    # Fetch curated free resources for missing skills
    curated_resources = []
    if missing_skills:
        # Search db for matching skill tags
        for missing in missing_skills:
            resources = db.query(LearningResource).filter(
                LearningResource.skill_tag.ilike(f"%{missing}%")
            ).all()
            for r in resources:
                curated_resources.append({
                    "skill": r.skill_tag,
                    "title": r.title,
                    "type": r.resource_type,
                    "url": r.url,
                    "est_hours": r.est_hours,
                    "description": r.description
                })

    # Fallback default high-yield resources if none in db
    if not curated_resources and missing_skills:
        for missing in missing_skills:
            curated_resources.append({
                "skill": missing,
                "title": f"Mastering {missing}: Complete Roadmap & Practical Guide",
                "type": "Interactive & Official Docs",
                "url": f"https://roadmap.sh",
                "est_hours": 12,
                "description": f"Comprehensive free curriculum and real-world project guide for {missing}."
            })

    # 5. Build 4-Week "Level-Up" Improvement Plan
    level_up_plan = generate_level_up_plan(student, drive, missing_skills, gaps)

    return {
        "is_eligible": is_eligible,
        "eligibility_status": "Eligible" if is_eligible else ("Borderline" if len(gaps) <= 2 and student.active_backlogs == 0 else "Ineligible"),
        "skill_match_pct": skill_match_pct,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "gaps_found": gaps,
        "strengths": strengths,
        "curated_free_resources": curated_resources,
        "level_up_plan": level_up_plan
    }


def generate_level_up_plan(student: Student, drive: CompanyDrive, missing_skills: List[str], gaps: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generates a personalized 4-week roadmap to elevate the student's current state to placement readiness.
    """
    missing_str = ", ".join(missing_skills[:3]) if missing_skills else "advanced system patterns"

    weeks = [
        {
            "week": 1,
            "theme": "Diagnostic Remediation & Fundamentals",
            "focus": f"Bridge theoretical gaps in {missing_str}",
            "tasks": [
                f"Complete modular overview of {missing_skills[0] if missing_skills else 'Data Structures & Algorithms'}",
                "Review past company placement drive questions and syntax fundamentals",
                "Set up local development sandbox and initialize clean repository"
            ],
            "milestone": "Pass self-assessment test with >75% accuracy."
        },
        {
            "week": 2,
            "theme": "Hands-On Implementation & Mini-Project",
            "focus": "Build verified proof-of-work project",
            "tasks": [
                f"Implement a production-ready feature utilizing {missing_str}",
                "Incorporate automated unit tests and structured logging",
                "Commit daily progress with descriptive atomic commit messages on GitHub"
            ],
            "milestone": "Live GitHub repository with working unit tests and comprehensive README."
        },
        {
            "week": 3,
            "theme": "Company-Specific Drive Drill & Resume Refactor",
            "focus": f"Align resume with {drive.company_name} criteria",
            "tasks": [
                f"Rewrite resume bullet points using Google's XYZ formula emphasizing {missing_str}",
                f"Solve 15 company-tagged questions frequently asked at {drive.company_name}",
                "Run GitHub Authenticity Audit to verify Proof-of-Work score > 80"
            ],
            "milestone": "ATS Match Score > 85% and Verified Project Badge active."
        },
        {
            "week": 4,
            "theme": "Mock Interview Simulation & Final Readiness",
            "focus": "Simulate actual interview pressure",
            "tasks": [
                f"Complete 2 AI Mock Interview sessions tailored to {drive.company_name}",
                "Practice STAR method storytelling for behavioral & technical tradeoffs",
                "Connect with a verified campus alumnus for a 15-minute quick prep check"
            ],
            "milestone": "Interview readiness score > 85% — Ready for Day 1 Campus Drive!"
        }
    ]

    return {
        "student_name": student.name,
        "target_company": drive.company_name,
        "target_role": drive.role_title,
        "estimated_hours_weekly": 10,
        "roadmap": weeks
    }
