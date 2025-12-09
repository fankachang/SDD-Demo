from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse, HTMLResponse
from sqlalchemy.orm import Session
import os

from . import db, models, schemas, emailer
from .api.releases import router as releases_router

app = FastAPI(title="Release Announcements MVP")


@app.on_event("startup")
def on_startup():
    # create DB tables if not present (MVP convenience)
    models.Base = db.Base  # ensure Base reference
    db.Base.metadata.create_all(bind=db.engine)


# register routers
app.include_router(releases_router)


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


@app.get("/send_logs", response_model=list[schemas.SendLogOut])
def list_send_logs(db: Session = Depends(get_db)):
    logs = db.query(models.SendLog).all()
    return logs
