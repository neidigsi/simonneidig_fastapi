"""
Work API Route for FastAPI

Author: Simon Neidig

This module provides the endpoint for retrieving "Work" entries via GET from `/work/`.
A "Work" represents a portfolio item or project shown on the website.
It supports language selection and returns a list of works.

Main features:
- Accepts GET requests to list works.
- Supports language selection via dependency injection.
"""

# Import external dependencies
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# Import internal dependencies
from app.db.models import work as models
from app.db.queries import work as crud
from app.db.database import engine
from app.schemas import work as schemas
from app.services.i18n import get_language
from app.services.db import get_db


models.Base.metadata.create_all(bind=engine)


# Create a new APIRouter instance for the work API
router = APIRouter(
    prefix="/work",
    tags=["work"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[schemas.Work])
async def get_works(lang: str = Depends(get_language), db: Session = Depends(get_db)):
    """
    Retrieves a list of work entries.

    Args:
        lang (str): Language code, injected via dependency.
        db (Session): Database session, injected via dependency.

    Returns:
        list[Work]: List of work items.

    """
    return crud.get_works(lang, db)
