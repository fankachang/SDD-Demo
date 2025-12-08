from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse, HTMLResponse
from sqlalchemy.orm import Session
import os

from . import db, models, schemas, emailer

app = FastAPI(title="Release Announcements MVP")


@app.on_event("startup")
def on_startup():
    # create DB tables if not present (MVP convenience)
    models.Base = db.Base  # ensure Base reference
    db.Base.metadata.create_all(bind=db.engine)


def get_db():
    db_session = db.SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()


@app.post("/auth/login")
def login(payload: schemas.LoginRequest):
    # Minimal stub: in MVP we trust authenticated environment or add later
    return {"message": "login not implemented in MVP; use dev stub"}


@app.get("/contacts", response_model=list[schemas.Contact])
def list_contacts(db: Session = Depends(get_db)):
    items = db.query(models.Contact).all()
    return items


@app.post("/contacts", status_code=201, response_model=schemas.Contact)
def create_contact(payload: schemas.Contact, db: Session = Depends(get_db)):
    contact = models.Contact(name=payload.name, email=str(payload.email), group=payload.group)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


@app.put("/contacts/{id}", response_model=schemas.Contact)
def update_contact(id: int, payload: schemas.Contact, db: Session = Depends(get_db)):
    contact = db.query(models.Contact).filter(models.Contact.id == id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    contact.name = payload.name
    contact.email = str(payload.email)
    contact.group = payload.group
    db.commit()
    db.refresh(contact)
    return contact


@app.delete("/contacts/{id}", status_code=204)
def delete_contact(id: int, db: Session = Depends(get_db)):
    contact = db.query(models.Contact).filter(models.Contact.id == id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(contact)
    db.commit()
    return JSONResponse(status_code=204, content=None)


@app.get("/programs", response_model=list[schemas.Program])
def list_programs(db: Session = Depends(get_db)):
    return db.query(models.Program).all()


@app.post("/programs", status_code=201, response_model=schemas.Program)
def create_program(payload: schemas.Program, db: Session = Depends(get_db)):
    p = models.Program(name=payload.name, description=payload.description)
    db.add(p)
    db.commit()
    db.refresh(p)
    return p


@app.post("/releases", status_code=201)
def create_release(payload: schemas.ReleaseCreate, db: Session = Depends(get_db)):
    if not payload.recipients or len(payload.recipients) == 0:
        raise HTTPException(status_code=400, detail="At least one recipient required")
    release = models.Release(program_id=payload.program_id, version=payload.version, notes=payload.notes)
    db.add(release)
    db.commit()
    db.refresh(release)

    # persist recipients snapshot
    for r in payload.recipients:
        rr = models.ReleaseRecipient(release_id=release.id, email=str(r.email), recipient_type=r.type)
        db.add(rr)
    db.commit()
    return {"id": release.id}


@app.get("/releases/{id}/preview", response_class=HTMLResponse)
def preview_release(id: int, db: Session = Depends(get_db)):
    release = db.query(models.Release).filter(models.Release.id == id).first()
    if not release:
        raise HTTPException(status_code=404, detail="Release not found")
    # simple template
    subject = f"Release: {release.version}"
    body = f"<h1>{subject}</h1><p>{release.notes or ''}</p>"
    return HTMLResponse(content=body)


@app.post("/releases/{id}/send")
def send_release(id: int, recipients: dict | None = None, db: Session = Depends(get_db)):
    release = db.query(models.Release).filter(models.Release.id == id).first()
    if not release:
        raise HTTPException(status_code=404, detail="Release not found")

    # load recipients from DB snapshot if not provided
    recs = []
    if recipients and isinstance(recipients, dict) and "recipients" in recipients:
        recs = recipients["recipients"]
    else:
        rows = db.query(models.ReleaseRecipient).filter(models.ReleaseRecipient.release_id == id).all()
        recs = [{"email": r.email, "type": r.recipient_type} for r in rows]

    if len(recs) > 500:
        raise HTTPException(status_code=400, detail="recipient count exceeds 500 for synchronous send")

    # render template
    subject = f"Release {release.version}"
    body_template = "{{ notes }}"
    context = {"notes": release.notes or ""}
    rendered = emailer.render_template(subject, body_template, context)

    # perform synchronous send
    results = emailer.send_synchronously(rendered["subject"], rendered["body"], recs)

    # store send log
    overall_result = "success"
    details = []
    for r in results:
        details.append(f"{r['email']}:{r['result']}")
        if r["result"] != "success":
            overall_result = "failure"

    log = models.SendLog(release_id=release.id, result=overall_result, detail=";".join(details))
    db.add(log)
    release.status = models.ReleaseStatus.sent if overall_result == "success" else release.status
    db.commit()
    db.refresh(log)

    return {"send_log_id": log.id, "results": results}


@app.get("/send_logs", response_model=list[schemas.SendLogOut])
def list_send_logs(db: Session = Depends(get_db)):
    logs = db.query(models.SendLog).all()
    return logs
