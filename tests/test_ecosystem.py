import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.database import SessionLocal
from backend.models import Student, CompanyDrive
from backend.services.criteria_engine import evaluate_eligibility_and_gaps
from backend.services.github_service import audit_github_profile
from backend.services.interview_service import get_mock_question, evaluate_mock_answer

client = TestClient(app)


def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["app"] == "CareerNexus"


def test_get_students():
    response = client.get("/api/students")
    assert response.status_code == 200
    students = response.json()
    assert len(students) >= 5
    assert any(s["name"] == "Aarav Sharma" for s in students)


def test_get_drives():
    response = client.get("/api/drives")
    assert response.status_code == 200
    drives = response.json()
    assert len(drives) >= 5
    assert any(d["company_name"] == "Amazon" for d in drives)


def test_eligibility_and_gap_analysis():
    db = SessionLocal()
    student = db.query(Student).filter(Student.name == "Priya Patel").first()
    drive = db.query(CompanyDrive).filter(CompanyDrive.company_name == "Amazon").first()

    assert student is not None
    assert drive is not None

    result = evaluate_eligibility_and_gaps(student, drive, db)
    db.close()

    assert result["is_eligible"] is False
    assert result["eligibility_status"] in ["Borderline", "Ineligible"]
    assert len(result["gaps_found"]) > 0
    assert len(result["curated_free_resources"]) > 0
    assert "roadmap" in result["level_up_plan"]


def test_github_authenticity_audit():
    # Test valid engineering project
    res_valid = audit_github_profile("aarav-dev", "distributed-cache-engine")
    assert res_valid["proof_of_work_score"] >= 75
    assert res_valid["verified_project_badge"] is True
    assert res_valid["is_tutorial_clone"] is False

    # Test copy-pasted tutorial clone
    res_clone = audit_github_profile("rohan-v", "netflix-clone-css")
    assert res_clone["is_tutorial_clone"] is True
    assert res_clone["verified_project_badge"] is False


def test_mock_interview_evaluation():
    q = get_mock_question("Amazon", "SDE-1", "behavioral")
    assert "question" in q

    answer = "When our service had high latency (Situation), my goal was to reduce p99 times (Task). I analyzed the query logs, introduced Redis caching, and refactored SQL joins (Action). As a result, latency dropped by 45% and system handled 2x traffic (Result)."
    eval_res = evaluate_mock_answer(q["question"], "behavioral", answer)
    assert eval_res["score"] >= 70
    assert "star_breakdown" in eval_res


def test_recruiter_reverse_pitch_search():
    response = client.post("/api/recruiter/reverse-pitch/search", json={
        "min_cgpa": 7.5,
        "verified_project_only": True
    })
    assert response.status_code == 200
    data = response.json()
    assert "candidates" in data
    assert all(c["cgpa"] >= 7.5 for c in data["candidates"])
    assert all(c["verified_project_badge"] is True for c in data["candidates"])


def test_auth_signup_and_login():
    import uuid
    test_email = f"test_{uuid.uuid4().hex[:6]}@college.edu"

    # 1. Sign up new student
    signup_res = client.post("/api/auth/signup", json={
        "name": "Neha Gupta",
        "email": test_email,
        "password": "secretPassword!",
        "role": "student",
        "department": "Computer Science",
        "cgpa": 8.7
    })
    assert signup_res.status_code == 200
    signup_data = signup_res.json()
    assert signup_data["status"] == "success"
    assert signup_data["user"]["name"] == "Neha Gupta"

    # 2. Login with created credentials
    login_res = client.post("/api/auth/login", json={
        "email": test_email,
        "password": "secretPassword!"
    })
    assert login_res.status_code == 200
    login_data = login_res.json()
    assert login_data["status"] == "success"
    assert login_data["user"]["email"] == test_email

    # 3. Test wrong password
    bad_login = client.post("/api/auth/login", json={
        "email": test_email,
        "password": "wrongPassword"
    })
    assert bad_login.status_code == 401
