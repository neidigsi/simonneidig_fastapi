"""
Contact API Route for FastAPI

Author: Simon Neidig <mail@simon-neidig.eu>

This module provides the endpoint for submitting contact requests via POST to `/contact/`.
A "Contact" represents a contact inquiry submitted via the website.
It validates input, handles errors, and persists contact data to the database.

Main features:
- Accepts POST requests with `name`, `email`, and `message`.
- Validates and parses input using Pydantic.
- Handles validation and database errors with appropriate HTTP responses.
- Supports language selection via dependency injection.
"""

# Import external dependencies
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import ValidationError

# Import internal dependencies
from app.db.queries.contact import save_contact
from app.schemas import contact as schemas
from app.services.i18n import get_language
from app.services.db import get_async_session


# Create a new APIRouter instance for the contact API
router = APIRouter(
    prefix="/contact",
    tags=["contact"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=schemas.SendingContact, status_code=201)
async def post_contact(
    request: Request,  # Use Request to manually parse the body
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Receives and processes a contact request.

    - Parses and validates the request body.
    - Checks for required fields.
    - Saves the contact to the database.
    - Returns the saved contact or an error message.

    Args:
        request (Request): FastAPI request object.
        lang (str): Language code, injected via dependency. Usually a iso 2 code is used.
        db (Session): Database session, injected via dependency.

    Returns:
        SendingContact: The saved contact data.

    Raises:
        HTTPException: On validation or database errors.
    """
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
        # Save the contact to the database (async helper)
        saved = await save_contact(contact, db, lang)
        return saved
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

