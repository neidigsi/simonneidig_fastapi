"""
Education API Route for FastAPI

Author: Simon Neidig <mail@simonneidig.de>

This module provides the endpoint for retrieving education entries via GET from `/education/`.
An "Education" represents an educational qualification or degree shown on the website.

Main features:
- Accepts GET requests to list education entries.
- Supports language selection via dependency injection.
"""

# Import external dependencies
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# Import internal dependencies
from app.db.models import education as models
from app.db.queries import education as crud
from app.db.database import engine
from app.schemas import education as schemas
from app.services.i18n import get_language
from app.services.db import get_async_session


router = APIRouter(
    prefix="/education",
    tags=["education"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[schemas.Education])
async def get_education(lang: str = Depends(get_language), db: Session = Depends(get_async_session)):
    """
    Retrieves a list of education entries.

    Args:
        lang (str): Language code, injected via dependency.
        db (Session): Database session, injected via dependency.

    Returns:
        list[Education]: List of education entries.
    """
    return crud.get_educations(lang, db)
