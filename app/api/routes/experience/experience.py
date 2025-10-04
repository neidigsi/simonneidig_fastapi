"""
Experience API Route for FastAPI

Author: Simon Neidig <mail@simon-neidig.eu>

This module provides the endpoint for retrieving experience entries via GET from `/experience/`.
An "Experience" represents a professional experience shown on the website.

Main features:
- Accepts GET requests to list experience entries.
- Supports language selection via dependency injection.
"""

# Import external dependencies
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

# Import internal dependencies
from app.db.queries import experience as crud
from app.schemas import experience as schemas
from app.services.i18n import get_language
from app.services.db import get_async_session
from app.services.user import fastapi_users


# dependency that enforces the current user to be a superuser
get_current_superuser = fastapi_users.current_user(superuser=True)


# Create a new APIRouter instance for the experience API
router = APIRouter(
    prefix="/experience",
    tags=["experience"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[schemas.ExperienceRead])
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


@router.post("/", response_model=schemas.ExperienceRead, status_code=status.HTTP_201_CREATED)
async def create_experience(
    payload: schemas.ExperienceCreate,
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_async_session),
    _admin=Depends(get_current_superuser),
    response: Response = None,
):
    """
    Create a new experience entry (admin only).

    Args:
        payload (ExperienceCreate): Payload validated against the ExperienceCreate schema.
        lang (str): Language code for the content to be created.
        db (AsyncSession): Async database session.
        _admin: Injected current user (must be superuser) — used for authorization only.
        response (Response): FastAPI Response object used to set headers.

    Returns:
        ExperienceRead: The created experience object serialized with the ExperienceRead schema.

    Raises:
        HTTPException(500): If creation failed for any reason.

    Notes:
        - On success, the response will include the 'Content-Language' header set to the requested language.
    """
    exp = await crud.create_experience(
        lang,
        db,
        title=payload.title,
        extract=payload.extract,
        description=payload.description,
        industry=payload.industry,
        url=payload.url,
        start_date=payload.start_date,
        end_date=payload.end_date,
        institution_id=payload.institution_id,
    )
    
    if not exp:
        raise HTTPException(status_code=500, detail="Failed to create experience")
    
    # set the language in the response headers so clients can easily detect the content language
    if response is not None:
        response.headers["Content-Language"] = lang
    
    return exp
