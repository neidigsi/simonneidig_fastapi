"""
PersonalInformation DB model for FastAPI

Author: Simon Neidig <mail@simon-neidig.eu>

This module defines short personal information items (e.g., location, email) that are intended
to be represented as key/value pairs and displayed on the website (e.g., sidebar/contact area).
"""

# Import external dependencies
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

# Import internal dependencies
from app.db.database import Base


class PersonalInformation(Base):
    __tablename__ = "personal_information"

    """
    Database object: PersonalInformation

    Represents a short piece of personal data, such as location or email, typically displayed
    as a key/value pair.

    Attributes:
        id (int): Primary key.
        icon (str): Icon identifier to visually represent the item.

    Relationships:
        translations: localized label/value pairs (PersonalInformationTranslation).
    """
    # Primary key
    id = Column(Integer, primary_key=True)

    # Content
    icon = Column(String)

    # Establishing relationships
    translations = relationship(
        "PersonalInformationTranslation", back_populates="personal_information")
