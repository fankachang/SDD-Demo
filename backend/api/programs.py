from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import db, models, schemas, auth

router = APIRouter()


@router.get("/programs", response_model=List[schemas.Program])
def list_programs(
    db: Session = Depends(db.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """列出所有程式（需登入）"""
    return db.query(models.Program).all()


@router.post("/programs", status_code=201, response_model=schemas.Program)
def create_program(
    payload: schemas.Program,
    db: Session = Depends(db.get_db),
    current_user: models.User = Depends(auth.get_current_admin)
):
    """建立程式（需 admin 權限）"""
    p = models.Program(name=payload.name, description=payload.description)
    db.add(p)
    db.commit()
    db.refresh(p)
    return p


@router.put("/programs/{id}", response_model=schemas.Program)
def update_program(
    id: int,
    payload: schemas.Program,
    db: Session = Depends(db.get_db),
    current_user: models.User = Depends(auth.get_current_admin)
):
    """更新程式（需 admin 權限）"""
    p = db.query(models.Program).filter(models.Program.id == id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Program not found")
    p.name = payload.name
    p.description = payload.description
    db.commit()
    db.refresh(p)
    return p


@router.delete("/programs/{id}", status_code=204)
def delete_program(
    id: int,
    db: Session = Depends(db.get_db),
    current_user: models.User = Depends(auth.get_current_admin)
):
    """刪除程式（需 admin 權限）"""
    p = db.query(models.Program).filter(models.Program.id == id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Program not found")
    db.delete(p)
    db.commit()
    return None
