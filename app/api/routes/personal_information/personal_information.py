"""
Personal Information API Route for FastAPI

Author: Simon Neidig <mail@simon-neidig.eu>

This module provides the endpoint for retrieving personal information via GET from `/personal-information/`.
A "PersonalInformation" entry represents short personal details such as location, email address, etc. displayed on the website.

Main features:
- Accepts GET requests to list personal information.
- Supports language selection via dependency injection.
"""

# Import external dependencies
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

# Import internal dependencies
from app.db.queries import personal_information as crud
from app.schemas import personal_information as schemas
from app.services.i18n import get_language
from app.services.db import get_async_session
from app.services.user import fastapi_users


# dependency that enforces the current user to be a superuser
get_current_superuser = fastapi_users.current_user(superuser=True)


# Create a new APIRouter instance for the personal information API
router = APIRouter(
    prefix="/personal-information",
    tags=["personal-information"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[schemas.PersonalInformationRead])
async def get_personal_information(lang: str = Depends(get_language), db: AsyncSession = Depends(get_async_session)):
    """
    Retrieves a list of personal information entries.

    Args:
        lang (str): Language code, injected via dependency.
        db (Session): Database session, injected via dependency.

    Returns:
        list[PersonalInformation]: List of personal information entries.
    """
    return await crud.get_personal_information(lang, db)


@router.post("/", response_model=schemas.PersonalInformationRead, status_code=status.HTTP_201_CREATED)
async def create_personal_information(
    payload: schemas.PersonalInformationCreate,
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_async_session),
    _admin=Depends(get_current_superuser),
    response: Response = None,
):
    """
    Create a new personal information entry (admin only).

    Args:
        payload (PersonalInformationCreate): Payload validated against the PersonalInformationCreate schema.
        lang (str): Language code for the content to be created.
        db (AsyncSession): Async database session.
        _admin: Injected current user (must be superuser) — used for authorization only.
        response (Response): FastAPI Response object used to set headers.

    Returns:
        PersonalInformationRead: The created expertise object serialized with the PersonalInformationRead schema.

    Raises:
        HTTPException(500): If creation failed for any reason.

    Notes:
        - On success, the response will include the 'Content-Language' header set to the requested language.
    """
    pi = await crud.create_personal_information(
        lang,
        db,
        label=payload.label,
        value=payload.value,
        icon=payload.icon,
    )
    
    if not pi:
        raise HTTPException(status_code=500, detail="Failed to create personal information")
    
    # set the language in the response headers so clients can easily detect the content language
    if response is not None:
        response.headers["Content-Language"] = lang
    
    return pi