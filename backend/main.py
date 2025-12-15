from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from . import db, models, schemas, auth
from .config import get_logger, cfg, redact_mapping
from .api.releases import router as releases_router
from .api import contacts as contacts_router
from .api import programs as programs_router
from .api import send_logs as send_logs_router

app = FastAPI(title="Release Announcements MVP")


@app.on_event("startup")
def on_startup():
    # create DB tables if not present (MVP convenience)
    models.Base = db.Base  # ensure Base reference
    # attach secret-redacting filter to root logger so logs don't leak secrets
    get_logger("")

    # log a redacted view of loaded config for debug (safe-printed)
    try:
        logger = get_logger(__name__)
        logger.info("Loaded config: %s", redact_mapping(cfg.as_dict()))
    except Exception:
        pass

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
def login(payload: schemas.LoginRequest, db: Session = Depends(db.get_db)):
    """使用者登入端點 - 驗證憑證並返回 access token"""
    logger = get_logger(__name__)

    # 驗證使用者
    user = auth.authenticate_user(db, payload.email, payload.password)
    if not user:
        logger.warning(f"登入失敗: {payload.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="帳號或密碼錯誤",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 建立 access token
    access_token = auth.create_session(
        user_id=user.id, user_email=user.email, user_role=user.role
    )

    logger.info(f"使用者登入成功: {user.email} (role: {user.role})")

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "role": user.role,
        },
    }


# contacts and programs routes are registered via routers in `backend/api/`


# send_logs endpoint is provided by backend/api/send_logs.py router
