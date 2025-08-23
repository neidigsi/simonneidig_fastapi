"""
PersonalDetails DB model for FastAPI

Author: Simon Neidig <mail@simonneidig.de>

This module defines detailed personal attributes (e.g., name, profile picture) that are
strictly defined fields rather than flexible key/value pairs.
"""

# Import external dependencies
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

# Import internal dependencies
from app.db.database import Base


class PersonalDetails(Base):
    __tablename__ = "personal_details"

    """
    Database object: PersonalDetails

    Represents fixed personal attributes for the site's owner/profile.

    Attributes:
        id (int): Primary key.
        name (str): Full name.
        profile_picture_id (int): FK to Image used as profile picture.

    Relationships:
        profile_picture: Image used as profile picture.
        translations: localized long-form fields (PersonalDetailsTranslation).
    """
    # Primary key
    id = Column(Integer, primary_key=True)

    # Content
    name = Column(String)
    profile_picture_id = Column(Integer, ForeignKey("image.id"))

    # Establishing relationships
    profile_picture = relationship(
        "Image", back_populates="personal_details"
    )
    translations = relationship(
        "PersonalDetailsTranslation", back_populates="personal_details")
