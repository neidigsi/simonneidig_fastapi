"""
Experience DB model for FastAPI

Author: Simon Neidig <mail@simonneidig.de>

This module defines professional/educational experiences which reference an Institution.
"""

# Import external dependencies
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

# Import internal dependencies
from app.db.database import Base


class Experience(Base):
    __tablename__ = "experience"

    """
    Database object: Experience

    Represents an employment or engagement period.

    Attributes:
        id (int): Primary key.
        start_date (date): Start date.
        end_date (date): End date.
        url (str): Optional URL for the company/project.
        institution_id (int): FK to Institution.

    Relationships:
        translations: localized texts for the experience.
        company: Institution linked to this experience.
    """
    # Primary key
    id = Column(Integer, primary_key=True)

    # Content
    start_date = Column(Date)
    end_date = Column(Date)
    url = Column(String)

    # Foreign keys
    institution_id = Column(Integer, ForeignKey("institution.id"))

    # Establishing relationships
    translations = relationship(
        "ExperienceTranslation", back_populates="experience")
    company = relationship("Institution", back_populates="experiences")
