"""
Image query helpers

Author: Simon Neidig <mail@simonneidig.de>

This module provides a small helper to retrieve Image model instances by their ID.
Images are stored on disk and referenced by other entities; this helper returns the
Image model (including filepath) so callers can serve or validate the file.
"""

# Import external dependencies
from sqlalchemy.orm import Session

# Import internal dependencies
from app.db.models.image import Image


def get_image(image_id: int, db: Session):
    """
    Retrieve an Image by its ID.

    Args:
        image_id (int): The ID of the image to retrieve.
        db (Session): SQLAlchemy database session.

    Returns:
        Image | None: The Image instance if found, otherwise None.
    """
    return db.query(Image).filter(Image.id == image_id).first()
