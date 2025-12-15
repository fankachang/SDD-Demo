from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import db, models, schemas, auth

router = APIRouter()


@router.get("/contacts", response_model=List[schemas.Contact])
def list_contacts(
    db: Session = Depends(db.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """列出所有聯絡人（需登入）"""
    return db.query(models.Contact).all()


@router.post("/contacts", status_code=201, response_model=schemas.Contact)
def create_contact(
    payload: schemas.Contact,
    db: Session = Depends(db.get_db),
    current_user: models.User = Depends(auth.get_current_admin)
):
    """建立聯絡人（需 admin 權限）"""
    contact = models.Contact(
        name=payload.name,
        email=str(payload.email),
        group=payload.group,
        created_by=current_user.id
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


@router.put("/contacts/{id}", response_model=schemas.Contact)
def update_contact(
    id: int,
    payload: schemas.Contact,
    db: Session = Depends(db.get_db),
    current_user: models.User = Depends(auth.get_current_admin)
):
    """更新聯絡人（需 admin 權限）"""
    contact = db.query(models.Contact).filter(models.Contact.id == id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    contact.name = payload.name
    contact.email = str(payload.email)
    contact.group = payload.group
    db.commit()
    db.refresh(contact)
    return contact


@router.delete("/contacts/{id}", status_code=204)
def delete_contact(
    id: int,
    db: Session = Depends(db.get_db),
    current_user: models.User = Depends(auth.get_current_admin)
):
    """刪除聯絡人（需 admin 權限）"""
    contact = db.query(models.Contact).filter(models.Contact.id == id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(contact)
    db.commit()
    return None
