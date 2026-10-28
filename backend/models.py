from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    role = Column(String(30), default="student")  # student, recruiter, tpo
    company = Column(String(100), default="")  # for recruiters
    student_id = Column(Integer, ForeignKey("students.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    roll_no = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    department = Column(String(100), nullable=False)  # Computer Science, Information Tech, etc.
    cgpa = Column(Float, nullable=False, default=7.0)
    graduation_year = Column(Integer, nullable=False, default=2026)
    active_backlogs = Column(Integer, nullable=False, default=0)
    skills = Column(Text, default="")  # comma-separated
    target_role = Column(String(100), default="Software Development Engineer")
    target_company = Column(String(100), default="Amazon")
    github_username = Column(String(100), default="")
    github_proof_score = Column(Integer, default=0)  # 0 to 100
    verified_project_badge = Column(Boolean, default=False)
    risk_level = Column(String(20), default="Moderate")  # Safe, Moderate, At-Risk
    placement_status = Column(String(50), default="Unplaced")  # Unplaced, Shortlisted, Offered, Placed
    resume_text = Column(Text, default="")

    applications = relationship("Application", back_populates="student", cascade="all, delete-orphan")
    mock_sessions = relationship("MockInterviewSession", back_populates="student", cascade="all, delete-orphan")
    alerts = relationship("PlacementAlert", back_populates="student", cascade="all, delete-orphan")


class CompanyDrive(Base):
    __tablename__ = "company_drives"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(100), nullable=False, index=True)
    role_title = Column(String(120), nullable=False)
    tier = Column(String(50), default="Dream")  # Super Dream, Dream, Standard
    ctc_lpa = Column(Float, nullable=False, default=12.0)
    min_cgpa = Column(Float, nullable=False, default=7.0)
    max_backlogs = Column(Integer, nullable=False, default=0)
    allowed_branches = Column(String(255), default="All")  # Comma separated or "All"
    required_skills = Column(Text, default="")  # Comma separated
    drive_date = Column(String(50), default="2026-11-15")
    deadline = Column(String(50), default="2026-11-01")
    status = Column(String(30), default="Open")  # Open, Ongoing, Closed
    description = Column(Text, default="")

    applications = relationship("Application", back_populates="drive", cascade="all, delete-orphan")


class DriveForensics(Base):
    __tablename__ = "drive_forensics"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(100), unique=True, nullable=False, index=True)
    rounds_json = Column(Text, default="[]")  # JSON array of round details
    frequent_topics = Column(String(255), default="")
    selection_rate = Column(Float, default=15.0)  # percentage
    interview_tips = Column(Text, default="")


class LearningResource(Base):
    __tablename__ = "learning_resources"

    id = Column(Integer, primary_key=True, index=True)
    skill_tag = Column(String(50), index=True, nullable=False)
    title = Column(String(200), nullable=False)
    resource_type = Column(String(50), default="Interactive Course")  # Documentation, YouTube, GitHub, Course
    url = Column(String(255), nullable=False)
    est_hours = Column(Integer, default=10)
    description = Column(Text, default="")


class Alumni(Base):
    __tablename__ = "alumni"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), nullable=False)
    current_company = Column(String(100), nullable=False, index=True)
    current_role = Column(String(120), nullable=False)
    graduation_batch = Column(Integer, nullable=False, default=2024)
    department = Column(String(100), nullable=False)
    linkedin_url = Column(String(255), default="")
    available_for_mock = Column(Boolean, default=True)
    referral_status = Column(String(30), default="Available")  # Available, Busy
    bio = Column(Text, default="")


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    drive_id = Column(Integer, ForeignKey("company_drives.id"), nullable=False)
    stage = Column(String(50), default="Applied")  # Applied, Online Assessment, Technical Round, HR Round, Offered, Rejected
    interview_date = Column(String(50), default="")
    notes = Column(Text, default="")
    ai_match_score = Column(Integer, default=70)  # 0 to 100
    is_reverse_pitch = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student", back_populates="applications")
    drive = relationship("CompanyDrive", back_populates="applications")


class MockInterviewSession(Base):
    __tablename__ = "mock_interview_sessions"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    company_name = Column(String(100), nullable=False)
    role = Column(String(100), nullable=False)
    category = Column(String(50), default="Technical")  # Technical, Behavioral - STAR, System Design
    question = Column(Text, nullable=False)
    student_answer = Column(Text, default="")
    score = Column(Integer, default=0)
    feedback = Column(Text, default="")
    model_answer = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student", back_populates="mock_sessions")


class PlacementAlert(Base):
    __tablename__ = "placement_alerts"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    title = Column(String(150), nullable=False)
    message = Column(Text, nullable=False)
    alert_type = Column(String(30), default="match")  # match, deadline, unlock, invite
    urgency = Column(String(20), default="medium")  # high, medium, info
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student", back_populates="alerts")


class RemediationCohort(Base):
    __tablename__ = "remediation_cohorts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)  # DSA, Aptitude, Core Web, System Design
    mentor = Column(String(100), default="Prof. Sharma (Placement Cell)")
    weekly_task = Column(Text, default="")
    student_ids = Column(Text, default="[]")  # JSON string array of student IDs
