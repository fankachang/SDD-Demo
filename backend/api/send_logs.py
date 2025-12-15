from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from .. import db, models, schemas, auth

router = APIRouter()


@router.get("/send_logs", response_model=List[schemas.SendLogOut])
def list_send_logs(
    program_id: Optional[int] = Query(None),
    start: Optional[datetime] = Query(None),
    end: Optional[datetime] = Query(None),
    result: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=500),
    db: Session = Depends(db.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """
    查詢發送紀錄（需登入）

    支援過濾：
    - program_id: 依程式篩選
    - start/end: 時間區間
    - result: 發送結果 (success/failure/timeout)
    - page/page_size: 分頁
    """
    q = db.query(models.SendLog)

    if program_id is not None:
        q = q.join(
            models.Release, models.SendLog.release_id == models.Release.id
        ).filter(models.Release.program_id == program_id)

    if result is not None:
        q = q.filter(models.SendLog.result == result)

    if start is not None:
        q = q.filter(models.SendLog.sent_at >= start)
    if end is not None:
        q = q.filter(models.SendLog.sent_at <= end)

    offset = (page - 1) * page_size
    logs = (
        q.order_by(models.SendLog.sent_at.desc()).offset(offset).limit(page_size).all()
    )
    return logs
