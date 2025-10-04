"""
ExperienceTranslation DB model for FastAPI

Author: Simon Neidig <mail@simon-neidig.eu>

This module defines localized fields for Experience entries (title, extract, description, industry).
"""

# Import external dependencies
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

# Import internal dependencies
from app.db.database import Base
from app.db.models.experience import Experience


class ExperienceTranslation(Base):
    __tablename__ = "experience_translation"

    """
    Database object: ExperienceTranslation

    Stores localized metadata for an Experience.

    Attributes:
        id (int): Primary key.
        title (str): Localized title.
        extract (str): Localized short extract.
        description (str): Localized full description.
        industry (str): Industry label.
        experience_id (int): FK to Experience.
        language_id (int): FK to Language.
    """
    # Primary key
    id = Column(Integer, primary_key=True)

    # Content
    title = Column(String)
    extract = Column(String)
    description = Column(String)
    industry = Column(String)

    # Foreign keys
    experience_id = Column(Integer, ForeignKey("experience.id"))
    language_id = Column(Integer, ForeignKey("language.id"))

    # Establishing relationships
    experience = relationship(
        "Experience", back_populates="translations")
    language = relationship(
        "Language", back_populates="experience_translations")
