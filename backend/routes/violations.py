from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from database import SessionLocal
from models import Violation, Video
from schemas import AIResult

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/ai-results")
def save_ai_results(data: AIResult, db: Session = Depends(get_db)):

    for v in data.violations:
        violation = Violation(
            video_id=data.video_id,
            type=v.type,
            timestamp=v.timestamp,
            confidence=v.confidence,
            image_path=v.image_path
        )
        db.add(violation)

    video = db.query(Video).filter(Video.id == data.video_id).first()
    if video:
        video.status = "completed"

    db.commit()

    return {"message": "Results stored"}


@router.get("/results/{video_id}")
def get_results(video_id: str, db: Session = Depends(get_db)):
    return db.query(Violation).filter(Violation.video_id == video_id).all()


@router.get("/violations")
def filter_violations(type: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Violation)

    if type:
        query = query.filter(Violation.type == type)

    return query.all()