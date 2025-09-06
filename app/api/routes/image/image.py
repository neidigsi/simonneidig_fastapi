"""
Image API Route for FastAPI

Author: Simon Neidig <mail@simonneidig.de>

This module provides the endpoint for retrieving images via GET from `/image/{image_id}`.
An "Image" represents an image file stored and referenced by the website.
Images can be used throughout the website in various objects. These objects return the image ID, and the actual image file can be retrieved via this route using that ID.

Main features:
- Accepts GET requests to retrieve images by ID.
- Returns image files from disk.
"""

# Import external dependencies
import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

# Import internal dependencies
from app.db.queries import image as crud
from app.services.db import get_async_session


# Create a new APIRouter instance for the image API
router = APIRouter(
    prefix="/image",
    tags=["image"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{image_id}", response_class=FileResponse)
async def get_image(image_id: int, db: AsyncSession = Depends(get_async_session)):
    """
    Retrieves an image file by its ID.

    Args:
        image_id (int): ID of the image.
        db (Session): Database session, injected via dependency.

    Returns:
        FileResponse: The image file.

    Raises:
        HTTPException: If the image or file is not found.
    """
    image = await crud.get_image(image_id, db)

    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    if not os.path.exists(image.filepath):
        raise HTTPException(
            status_code=404, detail="Image file missing on disk")

    # oder image/png
    return FileResponse(image.filepath, media_type="image/jpeg")
