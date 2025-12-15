from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, List
from pydantic import EmailStr, ValidationError
import re

from .. import db, models, schemas, emailer, auth
from ..services import release_service
from ..services import mailer as mailer_service
from ..config import get_logger

router = APIRouter()
logger = get_logger(__name__)


def validate_email_format(email: str) -> bool:
    """驗證 email 格式"""
    # 簡單的 email 正則表達式
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_recipients(recipients: List[Dict]) -> tuple[bool, List[str]]:
    """
    驗證收件人清單
    
    Returns:
        (is_valid, invalid_emails): 是否全部有效及無效的 email 清單
    """
    invalid_emails = []
    
    for recipient in recipients:
        email = recipient.get('email', '')
        if not email or not validate_email_format(email):
            invalid_emails.append(email)
    
    return len(invalid_emails) == 0, invalid_emails


@router.post("/releases", status_code=201)
def create_release(
    payload: schemas.ReleaseCreate,
    db: Session = Depends(db.get_db),
    current_user: models.User = Depends(auth.get_current_active_publisher)
):
    """建立 release 草稿（需 publisher 或 admin 權限）"""
    if not payload.recipients or len(payload.recipients) == 0:
        raise HTTPException(status_code=400, detail="At least one recipient required")
    
    # 將 created_by 設定為當前使用者
    release_data = payload.dict()
    release_data['created_by'] = current_user.id
    
    r = release_service.create_release(db, release_data)
    return {"id": r.id}


@router.get("/releases/{id}/preview")
def preview_release(
    id: int,
    db: Session = Depends(db.get_db),
    current_user: models.User = Depends(auth.get_current_active_publisher)
):
    """預覽 release 郵件內容（需 publisher 或 admin 權限）"""
    rendered = release_service.render_release_preview(db, id, emailer.render_template)
    if not rendered:
        raise HTTPException(status_code=404, detail="Release not found")
    return rendered["body"]


@router.post("/releases/{id}/send")
def send_release(
    id: int,
    recipients: Dict | None = None,
    db: Session = Depends(db.get_db),
    current_user: models.User = Depends(auth.get_current_active_publisher)
):
    """
    發送 release 郵件（同步）- 需 publisher 或 admin 權限
    
    驗證：
    - 收件人數量 <= 500
    - Email 格式正確
    - 30 秒 timeout
    """
    # load recipients
    recs = []
    if recipients and isinstance(recipients, dict) and "recipients" in recipients:
        recs = recipients["recipients"]
    else:
        rows = db.query(models.ReleaseRecipient).filter(models.ReleaseRecipient.release_id == id).all()
        recs = [{"email": r.email, "type": r.recipient_type} for r in rows]

    # 驗證收件人數量
    if len(recs) > 500:
        logger.warning(f"收件人數量超過限制: {len(recs)} > 500")
        raise HTTPException(
            status_code=400,
            detail={
                "error": "validation_error",
                "message": f"收件人數量超過限制",
                "details": {
                    "recipients": f"too_many_recipients: {len(recs)} > 500"
                }
            }
        )
    
    if len(recs) == 0:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "validation_error",
                "message": "至少需要一位收件人"
            }
        )
    
    # 驗證 email 格式
    is_valid, invalid_emails = validate_recipients(recs)
    if not is_valid:
        logger.warning(f"偵測到無效的 email 格式: {invalid_emails}")
        raise HTTPException(
            status_code=400,
            detail={
                "error": "validation_error",
                "message": "部分收件人 email 格式無效",
                "details": {
                    "invalid_emails": invalid_emails
                }
            }
        )

    try:
        result = mailer_service.send_release_synchronously(db, id, recs)
    except ValueError as e:
        logger.error(f"發送失敗: {e}")
        raise HTTPException(status_code=404, detail="Release not found")
    except TimeoutError:
        logger.error(f"發送 release {id} 超時")
        raise HTTPException(
            status_code=504,
            detail={
                "error": "timeout",
                "message": "SMTP request timed out (30s)"
            }
        )
    except Exception as e:
        logger.error(f"發送過程發生錯誤: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "internal_error",
                "message": "發送過程發生錯誤"
            }
        )

    return result
