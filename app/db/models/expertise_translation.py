"""
ExpertiseTranslation DB model for FastAPI

Author: Simon Neidig <mail@simonneidig.de>

This module defines localized title/description entries for Expertise.
"""

# Import external dependencies
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

# Import internal dependencies
from app.db.database import Base
from app.db.models.expertise import Expertise


class ExpertiseTranslation(Base):
    __tablename__ = "expertise_translation"

    """
    Database object: ExpertiseTranslation

    Stores localized title and description for an Expertise entry.

    Attributes:
        id (int): Primary key.
        title (str): Localized title.
        description (str): Localized description.
        expertise_id (int): FK to Expertise.
        language_id (int): FK to Language.
    """
    # Primary key
    id = Column(Integer, primary_key=True)

    # Content
    title = Column(String)
    description = Column(String)

    # Foreign keys
    expertise_id = Column(Integer, ForeignKey("expertise.id"))
    language_id = Column(Integer, ForeignKey("language.id"))

    # Establishing relationships
    expertise = relationship(
        "Expertise", back_populates="translations")
    language = relationship(
        "Language", back_populates="expertise_translations")
