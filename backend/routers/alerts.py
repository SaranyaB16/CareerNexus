from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Student, PlacementAlert
from backend.services.alert_service import generate_smart_alerts_for_student

router = APIRouter(prefix="/api/alerts", tags=["Placement Alerts"])


@router.get("/student/{student_id}", response_model=List[Dict[str, Any]])
def get_alerts_for_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return generate_smart_alerts_for_student(student, db)
