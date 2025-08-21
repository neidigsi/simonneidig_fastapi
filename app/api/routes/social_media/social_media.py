"""
Social Media API Route for FastAPI

Author: Simon Neidig <mail@simonneidig.de>

This module provides the endpoint for retrieving social media links via GET from `/social-media/`.
A "SocialMedia" entry represents a social media profile or link shown on the website.

Main features:
- Accepts GET requests to list social media links.
"""

# Import external dependencies
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# Import internal dependencies
from app.db.models import social_media as models
from app.db.queries import social_media as crud
from app.db.database import engine
from app.schemas import social_media as schemas
from app.services.db import get_db


models.Base.metadata.create_all(bind=engine)


# Create a new APIRouter instance for the social media API
router = APIRouter(
    prefix="/social-media",
    tags=["social media"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[schemas.SocialMedia])
async def get_social_medias(db: Session = Depends(get_db)):
    """
    Retrieves a list of social media entries.

    Args:
        db (Session): Database session, injected via dependency.

    Returns:
        list[SocialMedia]: List of social media links.
    """
    return crud.get_social_medias(db)
