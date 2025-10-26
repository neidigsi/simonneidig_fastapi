"""
Institution API Route for FastAPI

Author: Simon Neidig <mail@simon-neidig.eu>

This module provides the endpoint for retrieving institution entries via GET from `/institution/`.
An "Institution" represents a university or a company displayed on the website.

Main features:
- Accepts GET requests to list institution entries.
- Supports language selection via dependency injection.
"""

# Import external dependencies
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

# Import internal dependencies
from app.db.queries import institution as crud
from app.schemas import institution as schemas
from app.services.i18n import get_language
from app.services.db import get_async_session
from app.services.user import fastapi_users


# dependency that enforces the current user to be a superuser
get_current_superuser = fastapi_users.current_user(superuser=True)


# Create a new APIRouter instance for the institution API
router = APIRouter(
    prefix="/institution",
    tags=["institution"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[schemas.InstitutionRead])
async def get_institutions(lang: str = Depends(get_language), db: AsyncSession = Depends(get_async_session)):
    """
    Retrieves a list of institution entries.

    Args:
        lang (str): Language code, injected via dependency.
        db (Session): Database session, injected via dependency.

    Returns:
        list[Institution]: List of institution entries.
    """
    return await crud.get_institutions(lang, db)



@router.post("/", response_model=schemas.InstitutionRead, status_code=status.HTTP_201_CREATED)
async def create_institution(
    payload: schemas.InstitutionCreate,
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_async_session),
    _admin=Depends(get_current_superuser),
    response: Response = None,
):
    """
    Create a new institution entry (admin only).

    Args:
        payload (Institution): Payload validated against the Institution schema.
        lang (str): Language code for the content to be created.
        db (AsyncSession): Async database session.
        _admin: Injected current user (must be superuser) — used for authorization only.
        response (Response): FastAPI Response object used to set headers.

    Returns:
        Institution: The created institution object serialized with the Institution schema.

    Raises:
        HTTPException(500): If creation failed for any reason.

    Notes:
        - On success, the response will include the 'Content-Language' header set to the requested language.
    """
    inst = await crud.create_institution(
        lang,
        db,
        name=payload.name,
        address_id=payload.address_id,
    )
    
    if not inst:
        raise HTTPException(status_code=500, detail="Failed to create institution")
    
    # set the language in the response headers so clients can easily detect the content language
    if response is not None:
        response.headers["Content-Language"] = lang
    
    return inst
