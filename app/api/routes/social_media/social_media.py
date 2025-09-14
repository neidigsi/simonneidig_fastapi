"""
Social Media API Route for FastAPI

Author: Simon Neidig <mail@simonneidig.de>

This module provides the endpoint for retrieving social media links via GET from `/social-media/`.
A "SocialMedia" entry represents a social media profile or link shown on the website.

Main features:
- Accepts GET requests to list social media links.
"""

# Import external dependencies
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

# Import internal dependencies
from app.db.queries import social_media as crud
from app.schemas import social_media as schemas
from app.services.i18n import get_language
from app.services.db import get_async_session
from app.services.user import fastapi_users


# dependency that enforces the current user to be a superuser
get_current_superuser = fastapi_users.current_user(superuser=True)


# Create a new APIRouter instance for the social media API
router = APIRouter(
    prefix="/social-media",
    tags=["social media"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[schemas.SocialMediaRead])
async def get_social_medias(db: AsyncSession = Depends(get_async_session)):
    """
    Retrieves a list of social media entries.

    Args:
        db (Session): Database session, injected via dependency.

    Returns:
        list[SocialMedia]: List of social media links.
    """
    return await crud.get_social_medias(db)



@router.post("/", response_model=schemas.SocialMediaRead, status_code=status.HTTP_201_CREATED)
async def create_social_media(
    payload: schemas.SocialMediaCreate,
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_async_session),
    _admin=Depends(get_current_superuser),
    response: Response = None,
):
    """
    Create a new education entry (admin only).
    """
    sm = await crud.create_social_media(
        db,
        name=payload.name,
        url=payload.url,
        color=payload.color,
        path=payload.path
    )
    
    if not sm:
        raise HTTPException(status_code=500, detail="Failed to create social media")
    
        # set the language in the response headers so clients can easily detect the content language
    if response is not None:
        response.headers["Content-Language"] = lang
    
    return sm
