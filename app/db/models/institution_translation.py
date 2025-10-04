"""
InstitutionTranslation DB model for FastAPI

Author: Simon Neidig <mail@simon-neidig.eu>

This module defines localized names for Institution objects.
"""

# Import external dependencies
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

# Import internal dependencies
from app.db.database import Base


class InstitutionTranslation(Base):
    __tablename__ = "institution_translation"

    """
    Database object: InstitutionTranslation

    Stores the localized name for an Institution.

    Attributes:
        id (int): Primary key.
        name (str): Localized institution name.
        institution_id (int): FK to Institution.
        language_id (int): FK to Language.
    """
    # Primary key
    id = Column(Integer, primary_key=True)

    # Content
    name = Column(String)

    # Foreign keys
    institution_id = Column(Integer, ForeignKey("institution.id"))
    language_id = Column(Integer, ForeignKey("language.id"))

    # Establishing relationships
    institution = relationship(
        "Institution", back_populates="translations")
    language = relationship(
        "Language", back_populates="institution_translations")
