from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict

from .. import db, models, schemas, emailer
from ..services import release_service
from ..services import mailer as mailer_service

router = APIRouter()


@router.post("/releases", status_code=201)
def create_release(payload: schemas.ReleaseCreate, db: Session = Depends(db.get_db)):
    if not payload.recipients or len(payload.recipients) == 0:
        raise HTTPException(status_code=400, detail="At least one recipient required")
    r = release_service.create_release(db, payload.dict())
    return {"id": r.id}


@router.get("/releases/{id}/preview")
def preview_release(id: int, db: Session = Depends(db.get_db)):
    rendered = release_service.render_release_preview(db, id, emailer.render_template)
    if not rendered:
        raise HTTPException(status_code=404, detail="Release not found")
    return rendered["body"]


@router.post("/releases/{id}/send")
def send_release(id: int, recipients: Dict | None = None, db: Session = Depends(db.get_db)):
    # load recipients
    recs = []
    if recipients and isinstance(recipients, dict) and "recipients" in recipients:
        recs = recipients["recipients"]
    else:
        rows = db.query(models.ReleaseRecipient).filter(models.ReleaseRecipient.release_id == id).all()
        recs = [{"email": r.email, "type": r.recipient_type} for r in rows]

    if len(recs) > 500:
        raise HTTPException(status_code=400, detail="recipient count exceeds 500 for synchronous send")

    try:
        result = mailer_service.send_release_synchronously(db, id, recs)
    except ValueError:
        raise HTTPException(status_code=404, detail="Release not found")

    return result
