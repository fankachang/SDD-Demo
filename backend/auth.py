"""簡易授權中介層 - 提供 email/password 登入與 session 管理的 skeleton

此模組提供基本的授權功能：
1. 密碼雜湊與驗證
2. Session 管理（使用 JWT 或簡單的 in-memory store）
3. 角色驗證（admin, publisher）
4. 依賴注入與中介層函數

注意：這是 MVP 版本，生產環境需要更完善的安全機制
"""

import os
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict
from enum import Enum

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import jwt
from passlib.context import CryptContext

from backend.db import get_db
from backend.models import User
from backend.config import get_logger

logger = get_logger(__name__)

# 密碼雜湊設定
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT 設定
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("SESSION_EXPIRE_MINUTES", "60"))

# HTTP Bearer scheme
security = HTTPBearer()


class UserRole(str, Enum):
    """使用者角色定義"""

    ADMIN = "admin"
    PUBLISHER = "publisher"


def hash_password(password: str) -> str:
    """雜湊密碼"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """驗證密碼"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """建立 JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[Dict]:
    """解碼並驗證 JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        logger.warning("Token 已過期")
        return None
    except jwt.InvalidTokenError as e:
        logger.warning(f"JWT 驗證失敗: {e}")
        return None


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """驗證使用者憑證"""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """取得當前登入使用者（依賴注入）"""
    token = credentials.credentials
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="無效或過期的憑證",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id_str: str = payload.get("sub")
    if user_id_str is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="無效的憑證格式",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        user_id = int(user_id_str)
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="無效的使用者 ID",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="使用者不存在",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def get_current_active_publisher(
    current_user: User = Depends(get_current_user),
) -> User:
    """確保當前使用者至少是 publisher 角色"""
    if current_user.role not in [UserRole.PUBLISHER, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="需要 publisher 或更高權限"
        )
    return current_user


async def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    """確保當前使用者是 admin 角色"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="需要 admin 權限"
        )
    return current_user


# Optional: 簡單的 in-memory session store（僅用於開發測試）
# 生產環境應使用 Redis 或資料庫
_session_store: Dict[str, Dict] = {}


def create_session(user_id: int, user_email: str, user_role: str) -> str:
    """建立 session 並返回 token"""
    token_data = {
        "sub": str(user_id),  # sub 必須是字串
        "email": user_email,
        "role": user_role,
    }
    access_token = create_access_token(token_data)

    # 儲存到 in-memory store（可選）
    _session_store[access_token] = {
        "user_id": user_id,
        "email": user_email,
        "role": user_role,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    return access_token


def revoke_session(token: str) -> bool:
    """撤銷 session（登出）"""
    if token in _session_store:
        del _session_store[token]
        return True
    return False


def get_session_info(token: str) -> Optional[Dict]:
    """取得 session 資訊（從 in-memory store）"""
    return _session_store.get(token)
