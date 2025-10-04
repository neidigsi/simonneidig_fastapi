"""
Expertise DB model for FastAPI

Author: Simon Neidig <mail@simon-neidig.eu>

This module defines expertise/skill entries shown on the website, each with icon and sort order.
"""

# Import external dependencies
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

# Import internal dependencies
from app.db.database import Base


class Expertise(Base):
    __tablename__ = "expertise"

    """
    Database object: Expertise

    Represents a skill or area of expertise.

    Attributes:
        id (int): Primary key.
        icon (str): Icon identifier.
        sort (int): Sorting order.

    Relationships:
        translations: localized titles/descriptions (ExpertiseTranslation).
    """
    # Primary key
    id = Column(Integer, primary_key=True)

    # Content
    icon = Column(String)
    sort = Column(Integer)

    # Establishing relationships
    translations = relationship(
        "ExpertiseTranslation", back_populates="expertise")
