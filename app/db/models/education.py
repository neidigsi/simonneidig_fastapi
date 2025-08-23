"""
Education DB model for FastAPI

Author: Simon Neidig <mail@simonneidig.de>

This module defines educational records (degrees) linked to an Institution.
"""

# Import external dependencies
from sqlalchemy import Column, Double, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

# Import internal dependencies
from app.db.database import Base
from app.db.models.institution import Institution


class Education(Base):
    __tablename__ = "education"

    """
    Database object: Education

    Represents an educational qualification.

    Attributes:
        id (int): Primary key.
        start_date (date): Start date.
        end_date (date): End date.
        degree (str): Degree name.
        grade (float): Numeric grade (Double).
        institution_id (int): FK to Institution.

    Relationships:
        translations: localized course/description (EducationTranslation).
        university: Institution linked to this education.
    """
    # Primary key
    id = Column(Integer, primary_key=True)

    # Content
    start_date = Column(Date)
    end_date = Column(Date)
    degree = Column(String)
    grade = Column(Double)

    # Foreign keys
    institution_id = Column(Integer, ForeignKey("institution.id"))

    # Establishing relationships
    translations = relationship(
        "EducationTranslation", back_populates="education")
    university = relationship(Institution, back_populates="educations")
