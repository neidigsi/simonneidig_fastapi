"""
Page API Route for FastAPI

Author: Simon Neidig <mail@simonneidig.de>

This module provides endpoints for retrieving pages via GET from `/page/`.
A "Page" represents a content page displayed on the website. Pages are designed to be extendable views and can be used generically.

Main features:
- Accepts GET requests to list all pages or retrieve a single page by tech_key.
- Supports language selection via dependency injection.
"""

# Import external dependencies
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# Import internal dependencies
from app.db.models import page as models
from app.db.queries import page as crud
from app.db.database import engine
from app.schemas import page as schemas
from app.services.i18n import get_language
from app.services.db import get_db


models.Base.metadata.create_all(bind=engine)


# Create a new APIRouter instance for the page API
router = APIRouter(
    prefix="/page",
    tags=["page"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[schemas.Page])
async def get_pages(lang: str = Depends(get_language), db: Session = Depends(get_db)):
    """
    Retrieves a list of pages.

    Args:
        lang (str): Language code, injected via dependency.
        db (Session): Database session, injected via dependency.

    Returns:
        list[Page]: List of pages.
    """
    return crud.get_pages(lang, db)


@router.get("/{tech_key}", response_model=schemas.Page)
async def get_page(tech_key: str, lang: str = Depends(get_language), db: Session = Depends(get_db)):
    """
    Retrieves a single page by its technical key.

    Args:
        tech_key (str): Technical key of the page.
        lang (str): Language code, injected via dependency.
        db (Session): Database session, injected via dependency.

    Returns:
        Page: The requested page.

    Raises:
        HTTPException: If the page is not found.
    """
    page = crud.get_page(tech_key, lang, db)
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return page
