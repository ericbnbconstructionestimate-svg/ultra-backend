from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app import models
import csv, io

router = APIRouter(prefix="/campaigns", tags=["campaigns"])

@router.post("/upload")
def upload_campaign(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = file.file.read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(content))
    for row in reader:
        # minimal example: store email as campaign
        c = models.Campaign(name=row.get("email"), user_id=1)  # user_id=1 for dev
        db.add(c)
    db.commit()
    return {"id": "1", "message": "Campaign uploaded!"}

@router.post("/{campaign_id}/start")
def start_campaign(campaign_id: int, db: Session = Depends(get_db)):
    # Minimal stub: just return success
    return {"message": f"Campaign {campaign_id} started!"}
