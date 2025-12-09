from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse, HTMLResponse
from sqlalchemy.orm import Session
import os

from . import db, models, schemas, emailer
from .api.releases import router as releases_router
from .api import contacts as contacts_router
from .api import programs as programs_router
from .api import send_logs as send_logs_router

app = FastAPI(title="Release Announcements MVP")


@app.on_event("startup")
def on_startup():
    # create DB tables if not present (MVP convenience)
    models.Base = db.Base  # ensure Base reference
    db.Base.metadata.create_all(bind=db.engine)


# register routers
app.include_router(releases_router)
app.include_router(contacts_router.router)
app.include_router(programs_router.router)
app.include_router(send_logs_router.router)


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


# contacts and programs routes are registered via routers in `backend/api/`


# send_logs endpoint is provided by backend/api/send_logs.py router
