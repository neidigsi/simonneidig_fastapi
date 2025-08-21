"""
Personal Details API Route for FastAPI

Author: Simon Neidig <mail@simonneidig.de>

This module provides the endpoint for retrieving personal details via GET from `/personal-details/`.
"PersonalDetails" represents detailed personal data shown on the website.
Unlike "Personal Information", these attributes are not extendable as key-value pairs, but are strictly defined.

Main features:
- Accepts GET requests to retrieve personal details.
- Supports language selection via dependency injection.
"""

# Import external dependencies
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# Import internal dependencies
from app.db.models import personal_details as models
from app.db.queries import personal_details as crud
from app.db.database import engine
from app.schemas import personal_details as schemas
from app.services.i18n import get_language
from app.services.db import get_db


models.Base.metadata.create_all(bind=engine)


# Create a new APIRouter instance for the personal details API
router = APIRouter(
    prefix="/personal-details",
    tags=["personal-details"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=schemas.PersonalDetails)
async def get_personal_details(lang: str = Depends(get_language), db: Session = Depends(get_db)):
    """
    Retrieves personal details.

    Args:
        lang (str): Language code, injected via dependency.
        db (Session): Database session, injected via dependency.

    Returns:
        PersonalDetails: Detailed personal information.

    Raises:
        HTTPException: If no personal details are found.
    """
    personal_details = crud.get_personal_details(lang, db)
    if not personal_details:
        raise HTTPException(status_code=404, detail="Personal details not found")
    return personal_details
