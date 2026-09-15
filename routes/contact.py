from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from config import limiter, settings
from database import get_db
from models.contact import Contact
from schemas.contact import ContactCreate, ContactResponse

router = APIRouter()


@router.post("/contact", response_model=ContactResponse, status_code=201)
@limiter.limit(settings.CONTACT_RATE_LIMIT)
def create_contact(request: Request, payload: ContactCreate, db: Session = Depends(get_db)) -> Contact:
    contact = Contact(**payload.model_dump())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact
