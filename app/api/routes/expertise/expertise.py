"""
Expertise API Route for FastAPI

Author: Simon Neidig <mail@simon-neidig.eu>

This module provides the endpoint for retrieving expertise entries via GET from `/expertise/`.
An "Expertise" represents a skill or area of knowledge displayed on the website.

Main features:
- Accepts GET requests to list expertise entries.
- Supports language selection via dependency injection.
"""

# Import external dependencies
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

# Import internal dependencies
from app.db.queries import expertise as crud
from app.schemas import expertise as schemas
from app.services.i18n import get_language
from app.services.db import get_async_session
from app.services.user import fastapi_users


# dependency that enforces the current user to be a superuser
get_current_superuser = fastapi_users.current_user(superuser=True)


# Create a new APIRouter instance for the expertise API
router = APIRouter(
    prefix="/expertise",
    tags=["expertise"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[schemas.ExpertiseRead])
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



@router.post("/", response_model=schemas.ExpertiseRead, status_code=status.HTTP_201_CREATED)
async def create_expertise(
    payload: schemas.ExpertiseCreate,
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_async_session),
    _admin=Depends(get_current_superuser),
    response: Response = None,
):
    """
    Create a new expertise entry (admin only).

    Args:
        payload (ExpertiseCreate): Payload validated against the ExpertiseCreate schema.
        lang (str): Language code for the content to be created.
        db (AsyncSession): Async database session.
        _admin: Injected current user (must be superuser) — used for authorization only.
        response (Response): FastAPI Response object used to set headers.

    Returns:
        ExpertiseRead: The created expertise object serialized with the ExpertiseRead schema.

    Raises:
        HTTPException(500): If creation failed for any reason.

    Notes:
        - On success, the response will include the 'Content-Language' header set to the requested language.
    """
    exp = await crud.create_expertise(
        lang,
        db,
        title=payload.title,
        description=payload.description,
        icon=payload.icon,
        sort=payload.sort
    )
    
    if not exp:
        raise HTTPException(status_code=500, detail="Failed to create expertise")
    
    # set the language in the response headers so clients can easily detect the content language
    if response is not None:
        response.headers["Content-Language"] = lang
    
    return exp
