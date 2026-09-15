from typing import List

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from config import settings
from database import get_db
from models.knowledge import KnowledgeBase
from schemas.knowledge import KnowledgeCreate, KnowledgeResponse, KnowledgeUpdate

router = APIRouter()


def verify_admin(x_admin_key: str = Header(..., alias="X-Admin-Key")) -> None:
    """Guards knowledge-base management endpoints. This is a content
    management API, not a public one — every route below requires it."""
    if x_admin_key != settings.ADMIN_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid admin credentials.")


@router.get("/knowledge", response_model=List[KnowledgeResponse], dependencies=[Depends(verify_admin)])
def list_knowledge(db: Session = Depends(get_db)):
    return db.query(KnowledgeBase).order_by(KnowledgeBase.id).all()


@router.post("/knowledge", response_model=KnowledgeResponse, status_code=201, dependencies=[Depends(verify_admin)])
def create_knowledge(payload: KnowledgeCreate, db: Session = Depends(get_db)):
    entry = KnowledgeBase(**payload.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.put("/knowledge/{item_id}", response_model=KnowledgeResponse, dependencies=[Depends(verify_admin)])
def update_knowledge(item_id: int, payload: KnowledgeUpdate, db: Session = Depends(get_db)):
    entry = db.query(KnowledgeBase).filter(KnowledgeBase.id == item_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Knowledge entry not found.")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(entry, field, value)
    db.commit()
    db.refresh(entry)
    return entry


@router.delete("/knowledge/{item_id}", status_code=204, dependencies=[Depends(verify_admin)])
def delete_knowledge(item_id: int, db: Session = Depends(get_db)):
    entry = db.query(KnowledgeBase).filter(KnowledgeBase.id == item_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Knowledge entry not found.")
    db.delete(entry)
    db.commit()
    return None
