from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Student, MockInterviewSession
from backend.schemas import MockQuestionRequest, MockAnswerSubmit
from backend.services.interview_service import get_mock_question, evaluate_mock_answer

router = APIRouter(prefix="/api/mock-interview", tags=["Mock Interview Coach"])


@router.post("/generate-question")
def generate_question(payload: MockQuestionRequest, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == payload.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    q_data = get_mock_question(
        company=payload.company_name,
        role=payload.role,
        category=payload.category
    )

    session = MockInterviewSession(
        student_id=student.id,
        company_name=payload.company_name,
        role=payload.role,
        category=payload.category,
        question=q_data["question"]
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    return {
        "session_id": session.id,
        "company": payload.company_name,
        "role": payload.role,
        "category": payload.category,
        "question": q_data["question"],
        "rubric": q_data["rubric"]
    }


@router.post("/submit-answer")
def submit_answer(payload: MockAnswerSubmit, db: Session = Depends(get_db)):
    session = db.query(MockInterviewSession).filter(MockInterviewSession.id == payload.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Mock session not found")

    evaluation = evaluate_mock_answer(
        question=session.question,
        category=session.category,
        answer=payload.student_answer
    )

    session.student_answer = payload.student_answer
    session.score = evaluation["score"]
    session.feedback = "; ".join(evaluation["critique"])
    session.model_answer = evaluation["model_answer"]

    db.commit()
    db.refresh(session)

    return {
        "session_id": session.id,
        "score": evaluation["score"],
        "strengths": evaluation["strengths"],
        "critique": evaluation["critique"],
        "star_breakdown": evaluation["star_breakdown"],
        "model_answer": evaluation["model_answer"]
    }
