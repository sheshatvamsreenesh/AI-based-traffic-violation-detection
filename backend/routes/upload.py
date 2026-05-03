from fastapi import APIRouter, UploadFile, File, Depends
import shutil, uuid, os
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Video
from services.ai_client import send_to_ai

router = APIRouter()

UPLOAD_DIR = "storage"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/upload")
async def upload_video(file: UploadFile = File(...), db: Session = Depends(get_db)):
    video_id = str(uuid.uuid4())
    file_path = f"{UPLOAD_DIR}/{video_id}.mp4"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    video = Video(id=video_id, file_path=file_path, status="processing")
    db.add(video)
    db.commit()

    send_to_ai(video_id, file_path)

    return {"video_id": video_id, "status": "processing"}