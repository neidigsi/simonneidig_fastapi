"""
Image query helpers

Author: Simon Neidig <mail@simon-neidig.de>

This module provides a small helper to retrieve Image model instances by their ID.
Images are stored on disk and referenced by other entities; this helper returns the
Image model (including filepath) so callers can serve or validate the file.
"""

# Import external dependencies
from sqlalchemy.ext.asyncio import AsyncSession

# Import internal dependencies
from app.db.models.image import Image


async def get_image(image_id: int, db: AsyncSession):
    """
    Retrieve an Image by its ID.

    Args:
        image_id (int): The ID of the image to retrieve.
        db (AsyncSession): SQLAlchemy async database session.

    Returns:
        Image | None: The Image instance if found, otherwise None.
    """
    # Use AsyncSession.get to fetch by primary key without triggering sync IO
    return await db.get(Image, image_id)
