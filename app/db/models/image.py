"""
Image DB model for FastAPI

Author: Simon Neidig <mail@simonneidig.de>

This module defines the Image model representing image files stored for use across the site.
Images are referenced by other objects (works, profile, etc.) via their ID.
"""

# Import external dependencies
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

# Import internal dependencies
from app.db.database import Base
from app.db.models.personal_details import PersonalDetails


class Image(Base):
    __tablename__ = "image"

    """
    Database object: Image

    Represents an image file stored on disk and referenced by other entities.

    Attributes:
        id (int): Primary key.
        filename (str): Unique filename identifier.
        filepath (str): Absolute or relative file path on disk.

    Relationships:
        work: referenced as a thumbnail for Work.
        personal_details: referenced as profile picture.
    """
    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Content
    filename = Column(String, nullable=False, unique=True)
    filepath = Column(String, nullable=False)

    # Establishing relationships
    work = relationship(
        "Work", back_populates="thumbnail", uselist=False
    )
    personal_details = relationship(
        "PersonalDetails", back_populates="profile_picture", uselist=False
    )
