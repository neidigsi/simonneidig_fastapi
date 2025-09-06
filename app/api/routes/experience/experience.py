"""
Experience API Route for FastAPI

Author: Simon Neidig <mail@simonneidig.de>

This module provides the endpoint for retrieving experience entries via GET from `/experience/`.
An "Experience" represents a professional or educational experience shown on the website.

Main features:
- Accepts GET requests to list experience entries.
- Supports language selection via dependency injection.
"""

# Import external dependencies
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

# Import internal dependencies
from app.db.queries import experience as crud
from app.schemas import experience as schemas
from app.services.i18n import get_language
from app.services.db import get_async_session


# Create a new APIRouter instance for the experience API
router = APIRouter(
    prefix="/experience",
    tags=["experience"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[schemas.Experience])
async def get_experiences(lang: str = Depends(get_language), db: AsyncSession = Depends(get_async_session)):
    """
    Retrieves a list of experience entries.

    Args:
        lang (str): Language code, injected via dependency.
        db (Session): Database session, injected via dependency.

    Returns:
        list[Experience]: List of experience entries.
    """
    return await crud.get_experiences(lang, db)
