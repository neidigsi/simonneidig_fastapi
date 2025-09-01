"""
Personal Information API Route for FastAPI

Author: Simon Neidig <mail@simonneidig.de>

This module provides the endpoint for retrieving personal information via GET from `/personal-information/`.
A "PersonalInformation" entry represents short personal details such as location, email address, etc. displayed on the website.

Main features:
- Accepts GET requests to list personal information.
- Supports language selection via dependency injection.
"""

# Import external dependencies
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# Import internal dependencies
from app.db.models import personal_information as models
from app.db.queries import personal_information as crud
from app.db.database import engine
from app.schemas import personal_information as schemas
from app.services.i18n import get_language
from app.services.db import get_async_session


# Create a new APIRouter instance for the personal information API
router = APIRouter(
    prefix="/personal-information",
    tags=["personal-information"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[schemas.PersonalInformation])
async def get_personal_information(lang: str = Depends(get_language), db: Session = Depends(get_async_session)):
    """
    Retrieves a list of personal information entries.

    Args:
        lang (str): Language code, injected via dependency.
        db (Session): Database session, injected via dependency.

    Returns:
        list[PersonalInformation]: List of personal information entries.
    """
    return crud.get_personal_information(lang, db)
