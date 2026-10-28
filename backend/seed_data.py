import hashlib
import json
from backend.database import SessionLocal, init_db
from backend.models import (
    User, Student, CompanyDrive, DriveForensics,
    LearningResource, Alumni, RemediationCohort
)


def seed_database():
    init_db()
    db = SessionLocal()

    # Only seed if empty
    if db.query(Student).count() > 0:
        db.close()
        return

    # 1. Seed Students
    students = [
        Student(
            roll_no="22CS101",
            name="Aarav Sharma",
            email="aarav.sharma@college.edu",
            department="Computer Science",
            cgpa=8.8,
            graduation_year=2026,
            active_backlogs=0,
            skills="Python, FastAPI, Docker, PostgreSQL, React, Git",
            target_role="Software Development Engineer (SDE-1)",
            target_company="Amazon",
            github_username="aarav-sharma-dev",
            github_proof_score=88,
            verified_project_badge=True,
            risk_level="Safe",
            placement_status="Shortlisted"
        ),
        Student(
            roll_no="22IT104",
            name="Priya Patel",
            email="priya.patel@college.edu",
            department="Information Technology",
            cgpa=7.3,
            graduation_year=2026,
            active_backlogs=0,
            skills="Java, Spring Boot, MySQL, HTML/CSS",
            target_role="Backend Engineer",
            target_company="Microsoft",
            github_username="priya-codes",
            github_proof_score=62,
            verified_project_badge=False,
            risk_level="Moderate",
            placement_status="Unplaced"
        ),
        Student(
            roll_no="22EC209",
            name="Rohan Verma",
            email="rohan.verma@college.edu",
            department="Electronics & Communication",
            cgpa=6.4,
            graduation_year=2026,
            active_backlogs=1,
            skills="C++, Python, Basic SQL",
            target_role="Software Analyst",
            target_company="TCS Digital",
            github_username="rohan-verma",
            github_proof_score=45,
            verified_project_badge=False,
            risk_level="At-Risk",
            placement_status="Unplaced"
        ),
        Student(
            roll_no="22CS115",
            name="Ananya Iyer",
            email="ananya.iyer@college.edu",
            department="Computer Science",
            cgpa=9.3,
            graduation_year=2026,
            active_backlogs=0,
            skills="Go, Kubernetes, Python, Distributed Systems, Redis, Docker",
            target_role="Systems / Cloud Engineer",
            target_company="Google",
            github_username="ananya-systems",
            github_proof_score=94,
            verified_project_badge=True,
            risk_level="Safe",
            placement_status="Offered"
        ),
        Student(
            roll_no="22ME302",
            name="Karthik Nair",
            email="karthik.nair@college.edu",
            department="Mechanical Engineering",
            cgpa=6.9,
            graduation_year=2026,
            active_backlogs=0,
            skills="Python, Data Analysis, SQL, PowerBI",
            target_role="Technology Consultant",
            target_company="Deloitte",
            github_username="karthik-nair",
            github_proof_score=58,
            verified_project_badge=False,
            risk_level="Moderate",
            placement_status="Unplaced"
        )
    ]
    db.add_all(students)
    db.commit()

    # Seed Demo Users for Login
    demo_password_hash = hashlib.sha256("password123".encode("utf-8")).hexdigest()
    users = [
        User(
            name="Aarav Sharma",
            email="aarav.sharma@college.edu",
            password_hash=demo_password_hash,
            role="student",
            student_id=students[0].id
        ),
        User(
            name="Priya Patel",
            email="priya.patel@college.edu",
            password_hash=demo_password_hash,
            role="student",
            student_id=students[1].id
        ),
        User(
            name="Sarah Jenkins",
            email="recruiter@amazon.com",
            password_hash=demo_password_hash,
            role="recruiter",
            company="Amazon"
        ),
        User(
            name="Prof. R. Sharma",
            email="tpo@college.edu",
            password_hash=demo_password_hash,
            role="tpo",
            company="Campus Placement Cell"
        )
    ]
    db.add_all(users)

    # 2. Seed Company Drives
    drives = [
        CompanyDrive(
            company_name="Amazon",
            role_title="Software Development Engineer I (SDE-1)",
            tier="Super Dream",
            ctc_lpa=28.5,
            min_cgpa=7.5,
            max_backlogs=0,
            allowed_branches="Computer Science, Information Technology, Electronics & Communication",
            required_skills="Data Structures, Algorithms, System Design, Python, AWS, Distributed Systems",
            drive_date="2026-11-20",
            deadline="2026-11-05",
            status="Open",
            description="Global technology leader hiring for core AWS and Consumer retail engineering teams."
        ),
        CompanyDrive(
            company_name="Google",
            role_title="Associate Software Engineer",
            tier="Super Dream",
            ctc_lpa=32.0,
            min_cgpa=8.5,
            max_backlogs=0,
            allowed_branches="Computer Science, Information Technology",
            required_skills="Advanced Algorithms, C++, Go, Distributed Systems, Problem Solving",
            drive_date="2026-11-25",
            deadline="2026-11-08",
            status="Open",
            description="Developing large-scale software systems powering search, YouTube, and cloud infrastructure."
        ),
        CompanyDrive(
            company_name="Microsoft",
            role_title="Software Engineer",
            tier="Super Dream",
            ctc_lpa=26.0,
            min_cgpa=8.0,
            max_backlogs=0,
            allowed_branches="Computer Science, Information Technology, Electronics & Communication",
            required_skills="C#, Java, Cloud Architecture, Data Structures, SQL, Azure",
            drive_date="2026-11-18",
            deadline="2026-11-03",
            status="Open",
            description="Empowering organizations worldwide through modern cloud services, Azure, and Teams."
        ),
        CompanyDrive(
            company_name="TCS Digital",
            role_title="Digital Innovator / Systems Engineer",
            tier="Dream",
            ctc_lpa=9.0,
            min_cgpa=6.5,
            max_backlogs=1,
            allowed_branches="All",
            required_skills="Java, Python, Web Development, Cloud Basics, SQL",
            drive_date="2026-11-12",
            deadline="2026-11-01",
            status="Open",
            description="Specialized digital transformation and AI solutions unit within Tata Consultancy Services."
        ),
        CompanyDrive(
            company_name="Deloitte",
            role_title="Technology Analyst",
            tier="Standard",
            ctc_lpa=7.5,
            min_cgpa=6.5,
            max_backlogs=0,
            allowed_branches="All",
            required_skills="SQL, Python, Data Analytics, Agile, Problem Solving",
            drive_date="2026-11-15",
            deadline="2026-11-02",
            status="Open",
            description="Enterprise technology advisory and cloud implementation consulting."
        )
    ]
    db.add_all(drives)

    # 3. Seed Drive Forensics (Battle Cards)
    forensics = [
        DriveForensics(
            company_name="Amazon",
            selection_rate=14.5,
            frequent_topics="Graphs, Dynamic Programming, Tree Traversals, System Design (Caching & Idempotency), 16 Leadership Principles",
            rounds_json=json.dumps([
                {"round": 1, "name": "Online Assessment (OA)", "duration": "90 mins", "focus": "2 Coding Problems (Medium-Hard DP/Graph) + Work Style Behavioral Simulation"},
                {"round": 2, "name": "Technical Round 1", "duration": "60 mins", "focus": "Data Structures & Algorithm optimization + 2 Leadership Principle questions"},
                {"round": 3, "name": "Technical Round 2 (Bar Raiser)", "duration": "60 mins", "focus": "System Design, Edge Cases, Customer Obsession & Ownership STAR stories"},
                {"round": 4, "name": "Hiring Manager Round", "duration": "45 mins", "focus": "Cultural fit, Bias for Action, Deliver Results, Project deep-dive"}
            ]),
            interview_tips="Never jump into code immediately. Clarify boundary conditions, explain your time/space complexity upfront, and structure behavioral answers strictly with STAR."
        ),
        DriveForensics(
            company_name="Google",
            selection_rate=8.2,
            frequent_topics="Advanced Trees, Dijkstra/Graph Shortest Paths, Bit Manipulation, Clean Code, Googleyness",
            rounds_json=json.dumps([
                {"round": 1, "name": "Google Online Challenge (GOC)", "duration": "60 mins", "focus": "2 algorithmic problems testing mathematical & DP optimization"},
                {"round": 2, "name": "Coding Interview 1", "duration": "45 mins", "focus": "Data structures, writing production-clean code on Google Docs"},
                {"round": 3, "name": "Coding Interview 2", "duration": "45 mins", "focus": "Scalability, amortized analysis, recursion tree optimization"},
                {"round": 4, "name": "Googlyness & Leadership", "duration": "45 mins", "focus": "Intellectual humility, collaborative problem solving, handling ambiguity"}
            ]),
            interview_tips="Google interviewers evaluate how you think when stuck. Speak your thought process out loud and verify test cases manually before saying you are done."
        ),
        DriveForensics(
            company_name="Microsoft",
            selection_rate=18.0,
            frequent_topics="Linked Lists, Trees, String Manipulation, Concurrency, SQL Joins & Normalization",
            rounds_json=json.dumps([
                {"round": 1, "name": "Online Assessment", "duration": "75 mins", "focus": "3 Coding Questions (Easy, Medium, Medium)"},
                {"round": 2, "name": "Technical Interview 1", "duration": "45 mins", "focus": "Core CS Fundamentals (OS, DBMS, OOP) + Live Coding"},
                {"round": 3, "name": "Technical Interview 2", "duration": "45 mins", "focus": "Resume Project deep-dive and architectural tradeoffs"},
                {"round": 4, "name": "AA (As Appropriate) Round", "duration": "45 mins", "focus": "Executive leadership, learning agility, growth mindset"}
            ]),
            interview_tips="Emphasize growth mindset. If you don't know a technology, explain how your foundational understanding helps you pick it up rapidly."
        )
    ]
    db.add_all(forensics)

    # 4. Seed Curated Free Resources
    resources = [
        LearningResource(
            skill_tag="System Design",
            title="System Design Primer (By Donne Martin)",
            resource_type="GitHub Roadmap",
            url="https://github.com/donnemartin/system-design-primer",
            est_hours=20,
            description="Industry standard open-source guide to building scalable, distributed software systems."
        ),
        LearningResource(
            skill_tag="AWS",
            title="AWS Certified Cloud Practitioner & SDE Track",
            resource_type="FreeCodeCamp & YouTube",
            url="https://www.freecodecamp.org/news/aws-cloud-practitioner-study-guide/",
            est_hours=14,
            description="Complete full-length zero-to-hero cloud training covering S3, EC2, Lambda, DynamoDB."
        ),
        LearningResource(
            skill_tag="Data Structures",
            title="NeetCode 150 - Curated Coding Roadmap",
            resource_type="Interactive & YouTube",
            url="https://neetcode.io/practice",
            est_hours=40,
            description="Structured roadmap covering every pattern tested in product company campus drives."
        ),
        LearningResource(
            skill_tag="Docker",
            title="Docker & Containerization for Developers",
            resource_type="Official Documentation & Video",
            url="https://docs.docker.com/get-started/",
            est_hours=8,
            description="Hands-on guide to containerizing microservices, docker-compose, and multi-stage builds."
        ),
        LearningResource(
            skill_tag="Distributed Systems",
            title="MIT 6.824: Distributed Systems Online",
            resource_type="University Course & Labs",
            url="https://pdos.csail.mit.edu/6.824/",
            est_hours=35,
            description="World-renowned lecture notes and Go labs on Raft consensus, fault tolerance, and replication."
        )
    ]
    db.add_all(resources)

    # 5. Seed Alumni Mentors
    alumni_list = [
        Alumni(
            name="Siddharth Rao",
            email="siddharth.rao@amazon.com",
            current_company="Amazon",
            current_role="SDE-2 (AWS Elastic Compute)",
            graduation_batch=2023,
            department="Computer Science",
            linkedin_url="https://linkedin.com/in/siddharth-rao-dev",
            available_for_mock=True,
            referral_status="Available",
            bio="Alumnus from 2023 batch. Happy to conduct mock bar-raiser interviews and review resume bullets for junior batches."
        ),
        Alumni(
            name="Meera Krishnan",
            email="meerak@google.com",
            current_company="Google",
            current_role="Software Engineer (Search Infrastructure)",
            graduation_batch=2022,
            department="Computer Science",
            linkedin_url="https://linkedin.com/in/meera-krishnan-tech",
            available_for_mock=True,
            referral_status="Available",
            bio="Senior Engineer at Google. Mentoring students on algorithm optimization and preparing for GOC rounds."
        ),
        Alumni(
            name="Vikram Joshi",
            email="vikram.joshi@microsoft.com",
            current_company="Microsoft",
            current_role="Software Engineer 2 (Azure Cloud)",
            graduation_batch=2024,
            department="Information Technology",
            linkedin_url="https://linkedin.com/in/vikram-joshi-azure",
            available_for_mock=True,
            referral_status="Available",
            bio="Recent 2024 graduate. Can guide on how to clear Microsoft AA rounds and align resume with cloud projects."
        ),
        Alumni(
            name="Divya Sundaram",
            email="divya.sundaram@tcs.com",
            current_company="TCS Digital",
            current_role="Digital Solution Architect",
            graduation_batch=2023,
            department="Electronics & Communication",
            linkedin_url="https://linkedin.com/in/divya-sundaram",
            available_for_mock=True,
            referral_status="Available",
            bio="Transitioned from ECE to TCS Digital. Specializes in helping non-CS students crack top product/digital packages."
        )
    ]
    db.add_all(alumni_list)

    # 6. Seed Remediation Cohorts (for Placement Cell TPO)
    cohorts = [
        RemediationCohort(
            name="DSA & Competitive Coding Accelerator",
            category="DSA",
            mentor="Prof. R. Sharma (CSE Dept)",
            weekly_task="Solve 10 medium LeetCode problems on Binary Search and Trees by Friday 6 PM.",
            student_ids=json.dumps([2, 3])  # Priya, Rohan
        ),
        RemediationCohort(
            name="Aptitude & Speed Math Sprint",
            category="Aptitude",
            mentor="Dr. V. Gupta (Training Cell)",
            weekly_task="Complete 2 speed mock tests on quantitative aptitude and logical deduction.",
            student_ids=json.dumps([3, 5])  # Rohan, Karthik
        )
    ]
    db.add_all(cohorts)

    db.commit()
    db.close()
    print("Database successfully seeded with realistic campus placement records!")


if __name__ == "__main__":
    seed_database()
