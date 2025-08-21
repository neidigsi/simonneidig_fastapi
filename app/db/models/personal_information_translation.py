"""
PersonalInformationTranslation DB model for FastAPI

Author: Simon Neidig <mail@simonneidig.de>

This module defines localized label/value entries for PersonalInformation items.
"""

# Import external dependencies
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

# Import internal dependencies
from app.db.database import Base
from app.db.models.personal_information import PersonalInformation


class PersonalInformationTranslation(Base):
    __tablename__ = "personal_information_translation"

    """
    Database object: PersonalInformationTranslation

    Stores the localized label and value for a PersonalInformation item.

    Attributes:
        id (int): Primary key.
        label (str): Localized label (e.g., "Location", "Email").
        value (str): Localized value (e.g., "Paris", "mail@...").
        personal_information_id (int): FK to PersonalInformation.
        language_id (int): FK to Language.
    """
    # Primary key
    id = Column(Integer, primary_key=True)

    # Content
    label = Column(String)
    value = Column(String)

    # Foreign keys
    personal_information_id = Column(Integer, ForeignKey("personal_information.id"))
    language_id = Column(Integer, ForeignKey("language.id"))

    # Establishing relationships
    personal_information = relationship(
        "PersonalInformation", back_populates="translations")
    language = relationship(
        "Language", back_populates="personal_information_translations")
