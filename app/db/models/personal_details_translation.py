"""
PersonalDetailsTranslation DB model for FastAPI

Author: Simon Neidig <mail@simonneidig.de>

This module defines localized fields for PersonalDetails (e.g., position, abstract).
"""

# Import external dependencies
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

# Import internal dependencies
from app.db.database import Base
from app.db.models.personal_details import PersonalDetails


class PersonalDetailsTranslation(Base):
    __tablename__ = "personal_details_translation"

    """
    Database object: PersonalDetailsTranslation

    Stores localized long-form personal details such as position and abstract.

    Attributes:
        id (int): Primary key.
        position (str): Localized position/title.
        abstract (str): Localized bio/abstract.
        personal_details_id (int): FK to PersonalDetails.
        language_id (int): FK to Language.
    """
    # Primary key
    id = Column(Integer, primary_key=True)

    # Content
    position = Column(String)
    abstract = Column(String)

    # Foreign keys
    personal_details_id = Column(Integer, ForeignKey("personal_details.id"))
    language_id = Column(Integer, ForeignKey("language.id"))

    # Establishing relationships
    personal_details = relationship(
        "PersonalDetails", back_populates="translations")
    language = relationship(
        "Language", back_populates="personal_details_translations")
