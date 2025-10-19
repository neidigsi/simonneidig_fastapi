"""
Page API Route for FastAPI

Author: Simon Neidig <mail@simon-neidig.eu>

This module provides endpoints for retrieving pages via GET from `/page/`.
A "Page" represents a content page displayed on the website. Pages are designed to be extendable views and can be used generically.

Main features:
- Accepts GET requests to list all pages or retrieve a single page by tech_key.
- Supports language selection via dependency injection.
"""

# Import external dependencies
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

# Import internal dependencies
from app.db.queries import page as crud
from app.schemas import page as schemas
from app.services.i18n import get_language
from app.services.db import get_async_session
from app.services.user import fastapi_users


# dependency that enforces the current user to be a superuser
get_current_superuser = fastapi_users.current_user(superuser=True)


# Create a new APIRouter instance for the page API
router = APIRouter(
    prefix="/page",
    tags=["page"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[schemas.PageRead])
async def get_pages(lang: str = Depends(get_language), db: AsyncSession = Depends(get_async_session)):
    """
    Retrieves a list of pages.

    Args:
        lang (str): Language code, injected via dependency.
        db (Session): Database session, injected via dependency.

    Returns:
        list[Page]: List of pages.
    """
    return await crud.get_pages(lang, db)


@router.get("/{tech_key}", response_model=schemas.PageRead)
async def get_page(tech_key: str, lang: str = Depends(get_language), db: AsyncSession = Depends(get_async_session)):
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
    page = await crud.get_page(tech_key, lang, db)
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return page


@router.post("/", response_model=schemas.PageRead, status_code=status.HTTP_201_CREATED)
async def create_page(
    payload: schemas.PageCreate,
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_async_session),
    _admin=Depends(get_current_superuser),
    response: Response = None,
):
    """
    Create a new page entry (admin only).

    Args:
        payload (PageCreate): Payload validated against the PageCreate schema.
        lang (str): Language code for the content to be created.
        db (AsyncSession): Async database session.
        _admin: Injected current user (must be superuser) — used for authorization only.
        response (Response): FastAPI Response object used to set headers.

    Returns:
        PageRead: The created page object serialized with the PageCreate schema.

    Raises:
        HTTPException(500): If creation failed for any reason.

    Notes:
        - On success, the response will include the 'Content-Language' header set to the requested language.
    """
    p = await crud.create_page(
        lang,
        db,
        tech_key=payload.tech_key,
        title=payload.title,
        abstract=payload.abstract,
        html=payload.html,
        creation_date=datetime.now()
    )
    
    if not p:
        raise HTTPException(status_code=500, detail="Failed to create page")
    
    # set the language in the response headers so clients can easily detect the content language
    if response is not None:
        response.headers["Content-Language"] = lang
    
    return p
