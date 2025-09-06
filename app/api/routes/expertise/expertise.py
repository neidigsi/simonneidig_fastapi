"""
Expertise API Route for FastAPI

Author: Simon Neidig <mail@simonneidig.de>

This module provides the endpoint for retrieving expertise entries via GET from `/expertise/`.
An "Expertise" represents a skill or area of knowledge displayed on the website.

Main features:
- Accepts GET requests to list expertise entries.
- Supports language selection via dependency injection.
"""

# Import external dependencies
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

# Import internal dependencies
from app.db.queries import expertise as crud
from app.schemas import expertise as schemas
from app.services.i18n import get_language
from app.services.db import get_async_session


# Create a new APIRouter instance for the expertise API
router = APIRouter(
    prefix="/expertise",
    tags=["expertise"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[schemas.Expertise])
async def get_expertises(lang: str = Depends(get_language), db: AsyncSession = Depends(get_async_session)):
    """
    Retrieves a list of expertise entries.

    Args:
        lang (str): Language code, injected via dependency.
        db (Session): Database session, injected via dependency.

    Returns:
        list[Expertise]: List of expertise entries.
    """
    return await crud.get_expertises(lang, db)
