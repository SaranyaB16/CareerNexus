from typing import List, Optional
from pydantic import BaseModel


class StudentBase(BaseModel):
    roll_no: str
    name: str
    email: str
    department: str
    cgpa: float
    graduation_year: int = 2026
    active_backlogs: int = 0
    skills: str = ""
    target_role: str = "Software Development Engineer"
    target_company: str = "Amazon"
    github_username: str = ""
    github_proof_score: int = 0
    verified_project_badge: bool = False
    risk_level: str = "Moderate"
    placement_status: str = "Unplaced"
    resume_text: str = ""


class StudentCreate(StudentBase):
    pass


class StudentOut(StudentBase):
    id: int

    class Config:
        from_attributes = True


class CompanyDriveBase(BaseModel):
    company_name: str
    role_title: str
    tier: str = "Dream"
    ctc_lpa: float
    min_cgpa: float
    max_backlogs: int = 0
    allowed_branches: str = "All"
    required_skills: str = ""
    drive_date: str = "2026-11-15"
    deadline: str = "2026-11-01"
    status: str = "Open"
    description: str = ""


class CompanyDriveOut(CompanyDriveBase):
    id: int

    class Config:
        from_attributes = True


class ApplicationCreate(BaseModel):
    student_id: int
    drive_id: int
    stage: str = "Applied"
    notes: Optional[str] = ""


class ApplicationOut(BaseModel):
    id: int
    student_id: int
    drive_id: int
    stage: str
    interview_date: str
    notes: str
    ai_match_score: int
    is_reverse_pitch: bool

    class Config:
        from_attributes = True


class DiagnosticRequest(BaseModel):
    student_id: int
    company_id: int


class GitHubAuditRequest(BaseModel):
    student_id: int
    github_username: str
    sample_repo_url: Optional[str] = None


class MockQuestionRequest(BaseModel):
    student_id: int
    company_name: str
    role: str
    category: str = "Technical"  # Technical, Behavioral - STAR, System Design


class MockAnswerSubmit(BaseModel):
    session_id: int
    student_answer: str


class ReversePitchSearchRequest(BaseModel):
    skills: Optional[List[str]] = None
    min_cgpa: Optional[float] = None
    max_backlogs: Optional[int] = None
    department: Optional[str] = None
    verified_project_only: Optional[bool] = False


class ReversePitchInviteRequest(BaseModel):
    drive_id: int
    student_ids: List[int]
    custom_message: Optional[str] = None


class AlumniOut(BaseModel):
    id: int
    name: str
    email: str
    current_company: str
    current_role: str
    graduation_batch: int
    department: str
    linkedin_url: str
    available_for_mock: bool
    referral_status: str
    bio: str

    class Config:
        from_attributes = True


class AlumniMatchRequest(BaseModel):
    student_id: int
    target_company: Optional[str] = None
