# Import external dependencies
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import ValidationError

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


@router.post("/", response_model=schemas.SendingContact, status_code=201)
async def post_contact(
    request: Request,  # Use Request to manually parse the body
    lang: str = Depends(get_language),
    db: Session = Depends(get_db)
):
    try:
        # Parse and validate the request body
        body = await request.json()
        contact = schemas.SendingContact(**body)
    except ValidationError as e:
        # Extract and return only the 'msg' from the validation error
        error_msg = e.errors()[0].get("msg", "Invalid input")
        raise HTTPException(status_code=400, detail=error_msg)

    # Validate input fields
    if not contact.name or not contact.email or not contact.message:
        raise HTTPException(status_code=400, detail="All fields (name, email, message) are required.")

    try:
        # Save the contact to the database
        return save_contact(contact, db, lang)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

