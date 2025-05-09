# Import external dependencies
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# Import internal dependencies
from app.db.models import contact as models
from app.db.queries.contact import save_contact
from app.db.database import engine
from app.schemas import contact as schemas
from app.services.i18n import get_language

from app.services.db import get_db


models.Base.metadata.create_all(bind=engine)


router = APIRouter(
    prefix="/contact",
    tags=["contact"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=schemas.SendingContact)
async def post_contact(
    contact: schemas.SendingContact,
    lang: str = Depends(get_language),
    db: Session = Depends(get_db)
):
    # Validate input fields
    if not contact.name or not contact.email or not contact.message:
        raise HTTPException(status_code=400, detail="All fields (name, email, message) are required.")

    # Save the contact to the database
    return save_contact(contact, db, lang)

